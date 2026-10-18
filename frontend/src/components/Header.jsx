const PREFERENCE_LABELS = [
  ["preferred_brand", (v) => v],
  ["preferred_fuel", (v) => v],
  ["preferred_transmission", (v) => v],
  ["preferred_city", (v) => v],
  ["max_price_tnd", (v) => "up to " + Number(v).toLocaleString("en") + " TND"],
];

function preferenceChips(preferences) {
  if (!preferences) return [];
  const chips = [];
  for (const [key, format] of PREFERENCE_LABELS) {
    if (preferences[key] != null && preferences[key] !== "") chips.push(format(preferences[key]));
  }
  return [...chips, ...(preferences.favorite_models || [])];
}

export default function Header({ preferences, onNewChat }) {
  const chips = preferenceChips(preferences);
  return (
    <header>
      <div className="bar">
        <div className="brand">
          <span className="plate">CAR SCOUT</span>
          <small>Used cars in Tunisia</small>
        </div>
        <button className="ghost" type="button" onClick={onNewChat}>New chat</button>
      </div>
      {chips.length > 0 && (
        <div className="prefs">
          Remembered:
          {chips.map((text) => (
            <span className="chip" key={text}>{text}</span>
          ))}
        </div>
      )}
    </header>
  );
}
