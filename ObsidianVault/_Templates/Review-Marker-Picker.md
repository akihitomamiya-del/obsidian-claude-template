<%*
const markers = {
  "FLAG — rethink this": "%%FLAG: %%",
  "WEAK — unconvincing, rework or remove": "%%WEAK%%",
  "EXPAND — flesh out more": "%%EXPAND%%",
  "MERGE — combine with another page": "%%MERGE: [[]]%%",
  "CUT — remove this": "%%CUT%%"
};
const pick = await tp.system.suggester(
  Object.keys(markers),
  Object.values(markers),
  false,
  "Review marker"
);
if (pick) {
  // For FLAG and MERGE, place cursor inside the marker
  tR += pick;
}
%>