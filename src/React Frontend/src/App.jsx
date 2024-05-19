import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from './Navbar';
import './index.css';

function App() {
  const navigate = useNavigate();
  const [selectedRowIndex, setSelectedRowIndex] = useState(null); // State to track the selected row index

  const handleRowClick = (index, ticker) => {
    setSelectedRowIndex(index); // Set the selected row index
    navigate(`/ticker/${ticker}`, { state: { title: 'Financial Event Risk Analysis Tool', year: year } });
  };
  
  const [exampleHeadlines, setExampleHeadlines] = useState([
  "U.S. Approves $1.5 Billion Loan to Restart Michigan Nuclear Plant",
  "Biden Plans Sweeping Effort to Block Arctic Oil Drilling",
  "Jobs Report Looms What's Next for Energy Transfer Stock and Its 8% Dividend Yield?",
  "IEA Expects Global Oil-Demand Growth to Slow Further in 2025",
  "Environmentalists protest as Biden administration approves huge oil export terminal off Texas coast",,
  "Driven by China, Coal Plants Made a Comeback in 2023",
  "Energy Dept. Awards $6 Billion for Green Steel, Cement and Even Macaroni Factories",
  "U.S. Seeks to Boost Nuclear Power After Decades of Inertia",
  "With inflation stalling, the long-predicted storm clouds in the economy may actually be forming"]);

  const [year, setYear] = useState(2024);
  const [tableData, setTableData] = useState([]);
  const [error, setError] = useState('');
  const [headline, setHeadline] = useState('');
  // const [limit, setLimit] = useState('');
  const [model, setModel] = useState('cosine');
  const [tickers, setTickers] = useState([]);
  const [sector, setSector] = useState(0);
  const [isLoading, setIsLoading] = useState(false); // State to track loading status
  const [isAnalyzing, setIsAnalyzing] = useState(false); // State to track loading status
  const [analyzingCompany, setAnalyzingCompany] = useState(''); // State to track loading status
  const [abortController, setAbortController] = useState(null);


  const environment = "dev"
  const apiUrl = environment === "dev" ? "http://127.0.0.1:5000" : "https://finance-risk-toolkit-api-scx3vdzzxa-ue.a.run.app";

  const fetchExampleData = (e) => {
    e.preventDefault(); // Prevent default form submission behavior
    
    if (abortController) {
      abortController.abort(); // Abort any ongoing fetch operation
    }

    const newAbortController = new AbortController();
    setAbortController(newAbortController);
    setIsLoading(true); // Start loading

    const fetchEndpoint = `${apiUrl}/example`;
    fetch(fetchEndpoint)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      const parsedData = JSON.parse(data.data);
      setTableData(parsedData);
      setError('');
    })
    .catch(error => {
      console.error('Error fetching data:', error);
      setError('Failed to fetch data. Please try again later.');
    })
    .finally(() => {setIsLoading(false); setIsAnalyzing(false);});
  }
  
  useEffect(() => {
    fetchHeadlines();
    fetchTickers();
  }, []);

  const onChangeSector = (e) => {
    const newSector = e.target.value;
    setSector(newSector);
    // fetchTickers(newSector); // Pass new sector directly to the fetch function
  };

  const fetchHeadlines = async () => {
    setIsLoading(true);

    if (abortController) {
      abortController.abort(); // Abort any ongoing fetch operation
    }
  
    const newAbortController = new AbortController();
    setAbortController(newAbortController);

    try {
      const response = await fetch('https://gnews.io/api/v4/top-headlines?q=energy+sector&category=business&token=ae289a4a0a662da6d2aee99dfe8a9a43&lang=en&country=us');
      // const response = "";
      if (!response.ok) {
        throw new Error('Failed to fetch headlines');
      }
      throw new Error('Failed to fetch headlines');
      const data = await response.json();
      setExampleHeadlines(data.articles.map(article => article.title));
      data.articles.forEach(article => {
        console.log(article.title)
      });
    } catch (error) {
      // console.error('API key has run out of available calls. Error fetching headlines:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getBackgroundColor = (key, value) => {
    console.log(key);
    if (key === 'Highest Semantic Similarity') {
      const sentiment = parseFloat(value);
      if (!isNaN(sentiment)) {
        if (sentiment > 0.3) {
          return '#b5ffad';
        } else if (sentiment > 0.2) {
          return '#fffaad'; // Slightly darker yellow
        } else {
          return '#edb4b4';
        }
      }
    } else if (key === 'Semantic Similarity Evaluation') {
      if (value === "High Similarity") {
        return '#b5ffad';
      } else if (value === "Medium Similarity") {
        return '#fffaad'; // Slightly darker yellow
      } else if (value === "Low Similarity") {
        return '#edb4b4';
      }
    }
    return 'inherit'; // Default background color
  };

  function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]]; // Swap elements
    }
  }

  useEffect(() => {
    fetchTickers();
  }, [sector]);

  const fetchTickers = async () => {
    try {
      console.log(sector);
      const fetchEndpoint = `${apiUrl}/get-tickers?farma=${sector}`
      const response = await fetch(fetchEndpoint);
      const data = await response.json();
      
      console.log(data["tickers"]);
      shuffleArray(data["tickers"]); // Shuffle the array
      setTickers(data["tickers"]);
    } catch (e) {
      setTickers([]);
    }
  };


  const fetchEvents = async (e) => {  
    console.log("Fetching Events...")
    e.preventDefault();
    try {
      const response = await fetch(`${apiUrl}/get-events`);
      const data = await response.json();

      console.log(data)

    } catch (error) {
      // console.error('API key has run out of available calls. Error fetching headlines:', error);
    }
  };

  const fetchData = async () => {
    if (abortController) {
      abortController.abort(); // Abort any ongoing fetch operation
    }

    const newAbortController = new AbortController();
    setAbortController(newAbortController);

    setTableData([]);
    if (!headline) {
      setError('Headline is required');
      setIsLoading(false);
      return;
    }

    setIsLoading(true);
    setError('');

    for (const tickerSymbol of tickers) {
        try {
        setAnalyzingCompany(tickerSymbol);
        setIsAnalyzing(true);
        const fetchEndpoint = `${apiUrl}/analyze-company?ticker=${tickerSymbol}&year=${year}&model=${model}&headline=${headline}`;

        const response = await fetch(fetchEndpoint, { signal: newAbortController.signal });
        if (!response.ok) {
          throw new Error(`Failed to fetch data for ticker ${tickerSymbol}`);
        }

        const data = await response.json();
        
        const newEntry = {
          Ticker: data[0]["Ticker"],
          "Company Name": data[0]["Company Name"],
          "Fill Date": data[0]["Fill Date"],
          Year: data[0]["Year"],
          "Headline": headline,
          // "Highest Semantic Similarity": data[0]["Highest Similarity Score"],
          "Semantic Similarity Evaluation": data[0]["Similarity Evaluation"],
          "Risk Section Representative Segment": data[0]["Risk Section Representative Segment"],
        };
        if (data[0]["Ticker"] == null) {
            continue;
        }
        setTableData(prevData => [...prevData, newEntry]);
        setIsLoading(false);
        setIsAnalyzing(false);

        } catch (error) {
          console.error('Error:', error);
          // setError(`Error: ${error.message}`);
        } finally {
          // setIsLoading(false);
        }
      }
  };


  const handleDownloadCSV = () => {
    if (tableData.length === 0) {
      setError('No data available to download');
      return;
    }

    const csvContent = generateCSV(tableData);
    const csvBlob = new Blob([csvContent], { type: 'text/csv' });
    const csvUrl = URL.createObjectURL(csvBlob);

    // Create a temporary <a> element to trigger the download
    const downloadLink = document.createElement('a');
    downloadLink.href = csvUrl;
    downloadLink.download = 'financial_data.csv';
    document.body.appendChild(downloadLink);
    downloadLink.click();

    // Cleanup
    document.body.removeChild(downloadLink);
    URL.revokeObjectURL(csvUrl);
  };

  const generateCSV = (data) => {
    const csvRows = [];
    // Header row
    const headers = Object.keys(data[0]);
    csvRows.push(headers.join(','));

    // Data rows
    data.forEach((row) => {
      const values = headers.map((header) => {
        const escapedValue = ('"' + row[header] + '"').replace(/"/g, '""');
        return escapedValue;
      });
      csvRows.push(values.join(','));
    });

    return csvRows.join('\n');
  };

  
  return (
    <div className="App">
      <Navbar></Navbar>
      <header className="App-header"></header>
      <div className="container text-center mx-auto">
        <h1 className="text-xl font-semibold p-4 mb-2">Event Semantic Similarity Analysis With Company SEC 10-K Risk Factors</h1>
        <p className='mb-6'>
          This toolkit will analyze if a company has listed concerns related to the event in the risk section of their SEC 10-K. <br></br>
          Enter a news headline or label representing an <b>event</b> or select a top news headline below:
        </p>
        {/* Form for ticker and year input */}
        <form className="mb-4 flex flex-col sm:flex-row justify-center items-center mx-auto" >
          
          <div className="flex flex-col items-center w-1/3 p-4">
            <select 
                className="select select-bordered mb-2 w-96" 
                value={headline}
                onChange={(e) => setHeadline(e.target.value)}
              >
                <option value="">Select a current news headline or type one below</option>
                {exampleHeadlines.map((line, index) => (
                  <option key={index} value={line}>{line}</option>
                ))}
            </select>
            <textarea 
              type="text" 
              placeholder="Enter Headline Here" 
              className="input input-bordered h-24 w-96" 
              value={headline}
              onChange={(e) => setHeadline(e.target.value)} // Convert ticker to uppercase
            />
            {/* <div className='justify-center my-4'>
              <button type="submit" onClick={fetchEvents} className="btn btn-secondary">Fetch Events</button>
            </div> */}
          </div>
          
          <div className="flex flex-col items-center align-middle w-1/3 p-4">
            <p className='inline w-48'>Annual Report Year</p>
            <input 
              type="number" 
              placeholder="Enter Year Here" 
              className="input input-bordered w-48 mt-2 mb-4"
              value={year}
              onChange={(e) => setYear(e.target.value)}
            />
            <p className='inline w-52 mb-2'>Select Farma French Sector</p>
            <select 
                className="select select-bordered mb-2" 
                value={sector}
                onChange={onChangeSector}
              >
                <option key="0" value="0">All Sectors</option>
                <option key="1" value="1">Consumer</option>
                <option key="2" value="2">Manufacturing</option>
                <option key="3" value="3">HiTec</option>
                <option key="4" value="4">Health and Medical</option>
                <option key="5" value="5">Energy</option>
                <option key="6" value="6">Other including Finance</option>
            </select>
            <p className='inline w-52 mb-2'>Select Similarity Method</p>
            <select 
                className="select select-bordered mb-2" 
                value={model}
                onChange={(e) => setModel(e.target.value)}
              >
                {/* <option key="ensemble" value="ensemble">Ensemble Evaluation *Not Done*</option> */}
                <option key="cosine" value="cosine">Cosine Similarity</option>
                <option key="nlp" value="nlp">Natural Language Processing</option>
                {/* <option key="bert" value="bert">RoBERTa Model</option> */}
                <option key="jaccard" value="jaccard">Jaccard Similarity</option>
                <option key="tfidf" value="tfidf">TF-IDF</option>
            </select>
            <button type="button" className="btn btn-primary w-48" onClick={fetchData}>Analyze Headline</button>
          </div>
        </form>
        <form onSubmit={fetchExampleData} className="mb-4">
          <button type="submit" className="btn btn-secondary">Show Example Output</button>
        </form>

        {!isLoading && tableData.length > 0 && (
          <div className="p-4 mx-auto">
            <table className="text-center table w-full mt-4 border-solid border-2 overflow-x-scroll">
              <thead>
                <tr className="bg-gray-200">
                  {Object.keys(tableData[0]).map((key) => (
                    <th key={key}>{key}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {tableData.map((row, index) => (
                  <tr key={index} 
                      onClick={() => handleRowClick(index, row['Ticker'])}
                      className={selectedRowIndex === index ? "selected-row" : ""}
                  >
                    {Object.entries(row).map(([key, value], valueIndex) => (
                      <td key={valueIndex} style={{ backgroundColor: getBackgroundColor(key, value) }}>{value}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
            {isAnalyzing && <p className='m-2'>Analyzing: {analyzingCompany}...</p>}
          </div>
        )}
        {/* Button to download CSV */}
        {!isLoading && tableData.length > 0 && (
          <div className="mt-4 mb-4 text-center"> {/* Added mb-4 for margin bottom */}
          <button type="button" className="btn btn-primary w-48" onClick={handleDownloadCSV}>
            Download Data as CSV
          </button>
        </div>
        )}
      
      {isLoading && <p>Processing Headline...</p>}
      {error && <p className="text-red-500">{error}</p>}
      

        <div>
      </div>
      </div>
    </div>
  );
}
export default App;


// docker buildx build --platform linux/amd64 -t finance-toolkit-api .
// docker tag finance-toolkit-api gcr.io/bufn-capstone/finance-toolkit-api:latest
// docker push gcr.io/bufn-capstone/finance-toolkit-api:latest


// Unused
// docker build -t finance-toolkit-api .
// gcloud run deploy finance-toolkit-api --image gcr.io/bufn-capstone/finance-toolkit-api:latest --platform managed --allow-unauthenticated
// docker run --rm -p 8080:8080 finance-toolkit-api
// docker image inspect finance-toolkit-api