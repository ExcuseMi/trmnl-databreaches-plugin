function transform(input) {
  if (!input || !input.data || !Array.isArray(input.data)) {
    return { "data": [] };
  }
  
  // Create a copy of the data array to avoid modifying the original
  var sortedData = input.data.slice();
  
  // Sort by AddedDate descending (newest first)
  sortedData.sort(function(a, b) {
    var dateA = new Date(a.AddedDate || 0);
    var dateB = new Date(b.AddedDate || 0);
    return dateB - dateA; // Descending order
  });
  
  // Take first 20 elements and transform each one
  var limitedData = sortedData.slice(0, 20).map(function(item) {
    return {
      "AddedDate": item.AddedDate || "",
      "Description": item.Description || "",
      "Title": item.Title || "",
      "LogoPath": item.LogoPath || "",
      "PwnCount": item.PwnCount || 0,
      "DataClasses": Array.isArray(item.DataClasses) ? item.DataClasses : []
    };
  });
  
  return { 
    "data": limitedData 
  };
}