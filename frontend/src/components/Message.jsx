// Shows "site.tn/short/path…" instead of a very long address; the link itself stays complete.
function shortLabel(url) {
  try {
    const parsed = new URL(url);
    let path = decodeURIComponent(parsed.pathname + parsed.search).replace(/\/$/, "");
    if (path.length > 42) path = path.slice(0, 42) + "…";
    return parsed.hostname.replace(/^www\./, "") + path;
  } catch {
    return url;
  }
}

function Link({ url, label }) {
  return (
    <a href={url} title={url} target="_blank" rel="noopener noreferrer">
      {label || shortLabel(url)}
    </a>
  );
}

// Turns web addresses into links and **text** into bold.
// Claude sometimes writes these Markdown marks even when asked for plain text.
function withLinks(text) {
  const pattern = /\[([^\]\n]+)\]\((https?:\/\/[^\s<>")]+)\)|\*\*([^*\n]+)\*\*|https?:\/\/[^\s<>"]+/g;
  const parts = [];
  let position = 0;
  for (const match of text.matchAll(pattern)) {
    parts.push(text.slice(position, match.index));
    let used = match[0].length;
    if (match[2]) {
      parts.push(<Link key={match.index} url={match[2]} label={match[1]} />);
    } else if (match[3]) {
      parts.push(<strong key={match.index}>{match[3]}</strong>);
    } else {
      const url = match[0].replace(/[.,;:!?)\]*]+$/, "");
      parts.push(<Link key={match.index} url={url} />);
      used = url.length;
    }
    position = match.index + used;
  }
  parts.push(text.slice(position));
  return parts;
}

const CLASS_NAMES = {
  user: "message user",
  assistant: "message assistant",
  waiting: "message assistant waiting",
  error: "message assistant error",
  note: "note",
};

export default function Message({ kind, text }) {
  return (
    <div className={CLASS_NAMES[kind]} dir="auto">
      {kind === "assistant" ? withLinks(text) : text}
    </div>
  );
}
