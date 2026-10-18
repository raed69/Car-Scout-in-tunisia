const EXAMPLES = [
  "Find me a Golf 7 diesel under 60k in Tunis",
  "nheb clio 4 essence fi sfax, mouch akther men 35 alf",
  "Peugeot 208 automatique à Sousse",
];

export default function Welcome({ onPick }) {
  return (
    <section className="welcome">
      <h1>Which car are you looking for?</h1>
      <p>Ask in Darija, French or English. Car Scout searches Tunisian ad sites and answers with links.</p>
      <div className="examples">
        {EXAMPLES.map((text) => (
          <button className="example" type="button" dir="auto" key={text} onClick={() => onPick(text)}>
            {text}
          </button>
        ))}
      </div>
    </section>
  );
}
