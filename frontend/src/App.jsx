import { useEffect, useRef, useState } from "react";

import { askQuestion, loadConversation, loadPreferences } from "./api.js";
import Composer from "./components/Composer.jsx";
import Header from "./components/Header.jsx";
import Message from "./components/Message.jsx";
import Welcome from "./components/Welcome.jsx";

// The browser remembers which chat was open, so a reload brings it back.
const SAVED_CHAT_KEY = "car-scout-conversation-id";

function readSavedChat() {
  try {
    return localStorage.getItem(SAVED_CHAT_KEY);
  } catch {
    return null;
  }
}

function saveChat(conversationId) {
  try {
    localStorage.setItem(SAVED_CHAT_KEY, conversationId);
  } catch {
    // Private windows can block this. The chat still works, it just will not come back after a reload.
  }
}

function withIds(messages) {
  return messages.map((message) => ({ id: crypto.randomUUID(), ...message }));
}

export default function App() {
  const [savedChat] = useState(readSavedChat);
  const [conversationId, setConversationId] = useState(() => savedChat || crypto.randomUUID());
  const [messages, setMessages] = useState([]);
  const [restoring, setRestoring] = useState(Boolean(savedChat));
  const [preferences, setPreferences] = useState(null);
  const [busy, setBusy] = useState(false);
  const [draft, setDraft] = useState("");
  const scroller = useRef(null);
  const input = useRef(null);

  useEffect(() => {
    loadPreferences().then(setPreferences);
  }, []);

  const openChat = useRef(conversationId);
  useEffect(() => {
    openChat.current = conversationId;
    saveChat(conversationId);
  }, [conversationId]);

  useEffect(() => {
    if (!savedChat) return;
    let cancelled = false;
    loadConversation(savedChat).then((data) => {
      // Skip it if the user pressed "New chat" while it was loading.
      if (cancelled || openChat.current !== savedChat) return;
      const restored = withIds(
        (data?.messages || []).map((message) => ({ kind: message.role, text: message.content }))
      );
      const notes = withIds((data?.warnings || []).map((warning) => ({ kind: "note", text: warning })));
      // If the user already asked something while the chat was loading, keep their new messages after it.
      setMessages((current) => [...restored, ...notes, ...current]);
      setRestoring(false);
    });
    return () => {
      cancelled = true;
    };
  }, [savedChat]);

  useEffect(() => {
    scroller.current.scrollTop = scroller.current.scrollHeight;
  }, [messages, busy]);

  function addMessages(...added) {
    setMessages((current) => [...current, ...withIds(added)]);
  }

  async function send(question) {
    setBusy(true);
    addMessages({ kind: "user", text: question });
    try {
      const data = await askQuestion(question, conversationId);
      addMessages(
        { kind: "assistant", text: data.answer || "No answer came back. Try again." },
        ...(data.warnings || []).map((warning) => ({ kind: "note", text: warning }))
      );
      setPreferences(data.preferences);
    } catch (error) {
      addMessages({ kind: "error", text: error.message });
    } finally {
      setBusy(false);
      input.current.focus();
    }
  }

  function newChat() {
    if (busy) return;
    const newId = crypto.randomUUID();
    openChat.current = newId;
    setConversationId(newId);
    setMessages([]);
    setRestoring(false);
    input.current.focus();
  }

  // An example only fills the box, so no credit is spent until the user presses Send.
  function pickExample(text) {
    setDraft(text);
    input.current.focus();
  }

  return (
    <>
      <Header preferences={preferences} onNewChat={newChat} />
      <main ref={scroller}>
        <div className="thread">
          {restoring && messages.length === 0 && <Message kind="waiting" text="Loading your last chat" />}
          {!restoring && messages.length === 0 && <Welcome onPick={pickExample} />}
          {messages.map((message) => (
            <Message key={message.id} kind={message.kind} text={message.text} />
          ))}
          {busy && <Message kind="waiting" text="Searching" />}
        </div>
      </main>
      <Composer inputRef={input} value={draft} onChange={setDraft} onSend={send} busy={busy} />
    </>
  );
}
