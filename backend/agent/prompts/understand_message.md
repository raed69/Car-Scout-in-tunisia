Understand the user's intent and extract structured fields.

The user is looking for a used car in Tunisia and may write in Darija (Arabic or Latin letters), French, or English. Your output is used to build a web search, so fill only what the message actually says.

- Leave a field empty when the message does not mention it. Do not guess a budget, city, or year.
- You may fill the brand when the model makes it obvious (Golf is Volkswagen, Clio is Renault, 208 is Peugeot).
- Prices are in Tunisian dinars. "60k", "60 mille" and "60 alf" all mean 60000.
- Write fuel and transmission in French, as Tunisian ads do: essence, diesel, hybride, électrique; manuelle, automatique.
- Put anything useful that has no field of its own in notes, such as a second model to compare or a price the user wants checked.

Sometimes the message comes with saved preferences: the fuel, gearbox, city, or budget this user asked for in earlier chats. They are defaults for what the user left unsaid, because most people keep the same budget and city from one search to the next.

- When the message does not mention one of those fields, fill it from the saved preferences and add the field's name to assumed_from_preferences.
- What the message says always wins. If the user names a different fuel, city, or budget, use theirs and do not list the field as assumed.
- If the user says a field does not matter ("any fuel", "n'importe quelle ville", "ay blasa"), leave it empty.
- A question about one specific car or price, like the Polo example below, is not a new search. Leave the saved preferences out of it.

Examples:
- "Find me a Golf 7 diesel under 60k in Tunis" => brand=Volkswagen, model=Golf 7, fuel=diesel, max_price_tnd=60000, city=Tunis.
- "nheb clio 4 essence fi sfax, mouch akther men 35 alf" => brand=Renault, model=Clio 4, fuel=essence, city=Sfax, max_price_tnd=35000.
- "I want a student-friendly Clio 4 or 208" => brand=Renault, model=Clio 4, notes="Also considering Peugeot 208. Wants something affordable for a student."
- Saved preferences {"fuel": "diesel", "city": "Tunis", "max_price_tnd": 60000} with the message "now show me a Clio 4 essence" => brand=Renault, model=Clio 4, fuel=essence, city=Tunis, max_price_tnd=60000, assumed_from_preferences=["city", "max_price_tnd"].
- "Is 45k fair for a 2016 Polo with 120k km?" => brand=Volkswagen, model=Polo, year_min=2016, year_max=2016, notes="Wants to know if 45000 TND is a fair price at 120000 km."
