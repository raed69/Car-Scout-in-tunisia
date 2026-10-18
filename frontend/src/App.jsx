import { useEffect, useRef, useState } from "react";

import { askQuestion, loadPreferences } from "./api.js";
import Composer from "./components/Composer.jsx";
import Header from "./components/Header.jsx";
import Message from "./components/Message.jsx";
import Welcome from "./components/Welcome.jsx";

export default function App() {
  const [conversationId, setConversationId] = useState(() => crypto.randomUUID());
  const [messages, setMessages] = useState([]);
  const [preferences, setPreferences] = useState(null);
  const [busy, setBusy] = useState(false);
  const [draft, setDraft] = useState("");
  const scroller = useRef(null);
  const input = useRef(null);

  useEffect(() => {
    loadPreferences().then(setPreferences);
  }, []);

  useEffect(() => {
    scroller.current.scrollTop = scroller.current.scrollHeight;
  }, [messages, busy]);

  function addMessages(...added) {
    setMessages((current) => [...current, ...added.map((message) => ({ id: crypto.randomUUID(), ...message }))]);
  }

  async function send(question) {
    setBusy(true);
    addMessages({ kind: "user", text: question });
    try {
      const data = await askQuestion(question, conversationId);
      addMessages(
        { kind: "assistant", text: data.answer || "No answer came back. Try again." },
        ...(data.warnings || []).map((warning) => ({ kind: "note", text: "Not saved: " + warning }))
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
    setConversationId(crypto.randomUUID());
    setMessages([]);
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
          {messages.length === 0 && <Welcome onPick={pickExample} />}
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
