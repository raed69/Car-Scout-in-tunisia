import { useState } from "react";

const PRICE_LABELS = {
  cheap: "Cheap",
  fair: "Normal price",
  expensive: "Expensive",
};

function formatNumber(value) {
  return value.toLocaleString("fr-FR");
}

// One ad: its picture, the exact link under it, then what Car Scout read from the ad.
export default function CarCard({ card }) {
  const [imageFailed, setImageFailed] = useState(false);
  const facts = [card.year, card.mileage_km != null && `${formatNumber(card.mileage_km)} km`].filter(Boolean);

  return (
    <article className="car-card">
      <a className="car-photo" href={card.url} target="_blank" rel="noopener noreferrer" tabIndex={-1}>
        {card.image && !imageFailed ? (
          <img src={card.image} alt="" loading="lazy" referrerPolicy="no-referrer" onError={() => setImageFailed(true)} />
        ) : (
          <span aria-hidden="true">🚗</span>
        )}
      </a>
      <div className="car-body">
        <a className="car-link" href={card.url} title={card.url} target="_blank" rel="noopener noreferrer">
          {card.site || "Open ad"} ↗
        </a>
        <h3 dir="auto">{card.title}</h3>
        <div className="car-price">
          {card.price_tnd ? `${formatNumber(card.price_tnd)} DT` : "Price in the ad"}
          {card.price_check && <span className={`badge ${card.price_check}`}>{PRICE_LABELS[card.price_check]}</span>}
        </div>
        {facts.length > 0 && <div className="car-facts">{facts.join(" · ")}</div>}
        {card.note && (
          <p className="car-note" dir="auto">
            {card.note}
          </p>
        )}
      </div>
    </article>
  );
}
