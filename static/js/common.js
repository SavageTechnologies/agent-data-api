

function ExportCSV(fileName, data) {
    const csvContent = data.map(e => e.join(",")).join("\n");
    const blob = new Blob([csvContent], {type: "text/csv;charset=utf-8"});
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `${fileName}.csv`);
    document.body.appendChild(link);
    link.click();
    link.remove();
}

async function LoadLocalGoogleSearch(query, city, state, country, next) {
    const searchParams = new URLSearchParams();

    searchParams.set("query", query);
    if (city && city.length > 0) {
        searchParams.set("city", city);
    }
    if (state && state.length > 0) {
        searchParams.set("state", state);
    }
    if (country && country.length > 0) {
        searchParams.set("country", country);
    }
    if (next) {
        searchParams.set("next", next);
    }
    const response = await fetch(`/api/v1/search/google/?${searchParams.toString()}`,{
        method: "GET",
    })
    const responseJson = await response.json()
    return responseJson;
}
async function LoadLocalYoutubeSearch(query, next) {
    const searchParams = new URLSearchParams();

    searchParams.set("query", query);
    if (next) {
        searchParams.set("next", next);
    }
    const response = await fetch(`/api/v1/search/youtube/?${searchParams.toString()}`,{
        method: "GET",
    })
    const responseJson = await response.json()
    return responseJson;
}