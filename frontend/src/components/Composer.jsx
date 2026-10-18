import { useLayoutEffect } from "react";

export default function Composer({ inputRef, value, onChange, onSend, busy }) {
  // The box grows with the text, up to the max-height set in the CSS.
  useLayoutEffect(() => {
    const box = inputRef.current;
    box.style.height = "auto";
    box.style.height = box.scrollHeight + 2 + "px";
  }, [value, inputRef]);

  useLayoutEffect(() => {
    inputRef.current.focus();
  }, [inputRef]);

  function submit(event) {
    event.preventDefault();
    const question = value.trim();
    if (!question || busy) return;
    onChange("");
    onSend(question);
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey && !event.nativeEvent.isComposing) {
      submit(event);
    }
  }

  return (
    <footer>
      <form className="composer" onSubmit={submit}>
        <textarea
          ref={inputRef}
          rows={1}
          dir="auto"
          maxLength={2000}
          placeholder="Describe the car you want"
          aria-label="Your question"
          value={value}
          onChange={(event) => onChange(event.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button className="send" type="submit" disabled={busy}>Send</button>
      </form>
      <div className="hint">Enter sends, Shift+Enter makes a new line. Each question uses a little of your Claude credit.</div>
    </footer>
  );
}
