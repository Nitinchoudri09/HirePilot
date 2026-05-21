const API_KEY =
  "3d8bf8ea7cmsh5f418c37b9cd93bp1b1828jsne35e8a617068";

export const fetchJobs = async () => {
  const url =
    "https://jsearch.p.rapidapi.com/search?query=software developer in Bangalore&page=1&num_pages=1";

  const options = {
    method: "GET",
    headers: {
      "X-RapidAPI-Key": API_KEY,
      "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
    },
  };

  try {
    const response = await fetch(url, options);
    const result = await response.json();

    console.log(result);

    return result.data;
  } catch (error) {
    console.error(error);
    return [];
  }
};
