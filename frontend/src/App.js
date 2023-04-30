import './App.css';
import {useState} from 'react';
import { TextField, Box, Button, Radio, RadioGroup, FormControlLabel, Typography } from '@mui/material';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { Card, CardContent } from '@material-ui/core';
import axios from 'axios';
import logo from './logo.png';


function App() {
    const sampleData = [
        //{ id: '1', title: 'Document 1', url: 'http://example.com/document1', meta_info: 'Some meta info', anchor: ['anchor1', 'anchor2'], rank: '2' },
        //{ id: '2', title: 'Document 2', url: 'http://example.com/document2', meta_info: 'Some meta info', anchor: ['anchor3', 'anchor4'], rank: '1' },
        //{ id: '3', title: 'Document 3', url: 'http://example.com/document3', meta_info: 'Some meta info', anchor: ['anchor5', 'anchor6'], rank: '3' },
      ];

  const [value, setValue] = useState('');
  const [showResult, setShowResult] = useState(false);
  const [queryDisabled, setQueryDisabled] = useState(false);
  const [clusterDisabled, setClusterDisabled] = useState(false);
  const [final_data, setFinalData] = useState(sampleData);
//  const [final_data_google, setFinalDataGoogle] = useState(sampleData);
//  const [final_data_bing, setFinalDataBing] = useState(sampleData);
  const [open, setOpen] = useState(false);

  const iframeBingSrc = `https://www.bing.com/search?q=${value}`;
  const iframeGoogleSrc = `https://www.google.com/search?q=${value}`;

  const handleClear = async e => {
    setValue('');
    setFinalData([]);
  }

  const handleHelp = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const [radioValue, setRadioValue] = useState('page_ranking');
  const [radioRestValue, setRestRadioValue] = useState('');

  const handleRestRadioChange = (event) => {
    setRestRadioValue(event.target.value);
  }

  const handleRadioChange = (event) => {
    setRadioValue(event.target.value);
    if (event.target.value === 'hits') {
        setQueryDisabled(true);
        setClusterDisabled(true);
    } else {
        setQueryDisabled(false);
        setClusterDisabled(false);
    }
  };
  
  const handleTextInput = (v) => {
    setValue(v.target.value);
  }

  const handleTextInputChange = async e => {
    if(value.length == 0) {
        alert("Input cannot be empty, Please enter a non-empty string!")
        return
    }
    let obj = {"config": radioValue, "rest": radioRestValue, "query":value}
    const response = await fetch(`http://127.0.0.1:8081/api/search`, {
            method: 'POST',
            crossDomain:true,
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(obj)
          })
    const result = await response.json()
          console.log(typeof result)
    
    // Sort the documents by rank
    setFinalData(result.result)
    final_data.sort((a, b) => a.rank - b.rank);
    setShowResult(true);
  }

  return (
    <div className="App">
      {/*<p>
        <code>Dive Search Engine</code>
      </p>*/}
      <header className="App-header">
      <Box
      component="form"
      sx={{
        '& > :not(style)': { m: 1, width: '50ch' },
      }}
      noValidate
      autoComplete="off"
    >
        <Box
      component="form"
      sx={{
        '& > :not(style)': { m: 1, width: '25ch', height: '20' },
      }}
      noValidate
      autoComplete="off"
    >
        <img src={logo} alt="logo" style={{ marginRight: 16 }} />
        <TextField className="search-bar" style={{ flex: 2, marginRight: 16 }} id="search" label="Enter text to search" multiline rows={value} onChange={handleTextInput} variant="outlined" color="primary"/>
        <div className="config-box" style={{  width: '100%', height: '100%' }}>
        <Box style={{ flex: 1, border: '1px solid black', borderRadius: 8, padding: 16 }}>
        <div style={{ display: 'flex', flexDirection: 'row', width: '100%', height: '100%' }}>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%', height: '100%' }}>
        <Typography variant="h6" gutterBottom color="primary">
          Configuration
        </Typography>
        <RadioGroup
        style={{ flex: 1 }}
        aria-label="radio-button"
        name="radio-button-group"
        value={radioValue}
        onChange={handleRadioChange}
      >
        <FormControlLabel
          value="page_ranking"
          control={<Radio color="primary"/>}
          label="Page Ranking"
        />
        <FormControlLabel
          value="hits"
          control={<Radio color="primary"/>}
          label="HITS"
        />
        </RadioGroup>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%', height: '100%' }}>
        <Typography variant="h6" gutterBottom color="primary">
        Clustering
        </Typography>
        <RadioGroup
        style={{ flex: 1 }}
        aria-label="radio-button"
        name="radio-button-group"
        value={radioRestValue}
        onChange={handleRestRadioChange}
      >
        <FormControlLabel
          value="flat_clustering"
          control={<Radio color="primary"/>}
          label="Flat clustering (KMeans)"
          disabled={clusterDisabled}
        />
        <FormControlLabel
          value="single_link"
          control={<Radio color="primary"/>}
          label="Agglomerative (Single link)"
          disabled={clusterDisabled}
        />
        <FormControlLabel
          value="centroid"
          control={<Radio color="primary"/>}
          label="Agglomerative (Centroid)"
          disabled={clusterDisabled}
        />
        </RadioGroup>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%', height: '100%' }}>
        <Typography variant="h6" gutterBottom color="primary">
        Query expansion
        </Typography>
        <RadioGroup
        style={{ flex: 1 }}
        aria-label="radio-button"
        name="radio-button-group"
        value={radioRestValue}
        onChange={handleRestRadioChange}
      >
        <FormControlLabel
          value="rocchio_algorithm"
          control={<Radio color="primary"/>}
          label="Rocchio algorithm"
          disabled={queryDisabled}
        />
        <FormControlLabel
          value="associative_cluster"
          control={<Radio color="primary"/>}
          label="Associative clusters"
          disabled={queryDisabled}
        />
        <FormControlLabel
          value="metric_cluster"
          control={<Radio color="primary"/>}
          label="Metric clusters"
          disabled={queryDisabled}
        />
        <FormControlLabel
          value="scalar_cluster"
          control={<Radio color="primary"/>}
          label="Scalar clusters"
          disabled={queryDisabled}
        />
        </RadioGroup>
        </div>
        </div>
        </Box>
        </div>
        </Box>
        <Box
      component="form"
      sx={{
        '& > :not(style)': { m: 1, width: '25ch' },
      }}
      noValidate
      autoComplete="off"
    >
        <Button variant="contained" onClick={handleTextInputChange}>Search</Button>
        <Button variant="contained" onClick={handleClear}>Clear</Button>
        <Button variant="contained" onClick={handleHelp}>Help</Button>
        <Dialog
        open={open}
        keepMounted
        onClose={handleClose}
        aria-describedby="alert-dialog-slide-description"
      >
        <DialogTitle>{"Help?"}</DialogTitle>
          <DialogContent>
            <DialogContentText id="alert-dialog-slide-description">
              <li>Input a text to search the web</li>
              <li>Select the configuration you need</li>
              <li>Click on 'search' to see the output</li>
              <li>Click on the clear button if you wish to clear the output</li>
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose}>Ok</Button>
          </DialogActions>
        </Dialog>
        </Box>
        </Box>
        {showResult && (
        <div className="result-box" style={{ display: 'flex', width: '100%', height: '100%' }}>
            <p>Results</p>
        <div style={{ display: 'flex', width: '100%', height: '100%' }}>
            <div className="result-box" style={{ flex: 1,  width: '100%', height: '100%' }}>
                <Box style={{ flex: 1, marginLeft: 15, marginRight: 15, border: '1px solid black', borderRadius: 8, padding: 16 }}>
                <Typography variant="h6" gutterBottom color="primary">
                  Our results
                </Typography>
                    {final_data.map((doc) => (
                      <Card key={doc.id} style={{ marginTop: 16 }}>
                        <CardContent>
                          <Typography variant="h6" component="h2">
                            <a href={doc.url} target="_blank" rel="noopener noreferrer">
                              {doc.title}
                            </a>
                          </Typography>
                          <Typography variant="subtitle1" color="textSecondary">
                          {doc.meta_info.split(' ').slice(0, 20).join(' ')}...
                          </Typography>
                        </CardContent>
                      </Card>
                    ))}
                </Box>
            </div>
            <div className="result-box" style={{ display: 'flex', flexDirection: 'column', flex: 1, width: '100%', height: '100%' }}>
                <div style={{ flex: 1, width: '100%', height: '100%' }}>
                    <Box style={{ flex: 1, border: '1px solid black', marginRight: 15, borderRadius: 8, padding: 16 }}>
                    <Typography variant="h6" gutterBottom color="primary">
                      Google results
                    </Typography>
                    <iframe src={iframeGoogleSrc} allow="autoplay; fullscreen; encrypted-media" style={{ width: '100%', height: '100vh', border: '1px solid black' }}></iframe>
                    </Box>
                </div>
                <div style={{ flex: 1, width: '100%', height: '100%' }}>
                    <Box style={{ flex: 1, border: '1px solid black', marginTop: 15, marginRight: 15, borderRadius: 8, padding: 16 }}>
                    <Typography variant="h6" gutterBottom color="primary">
                      Bing results
                    </Typography>
                    <iframe src={iframeBingSrc} allow="autoplay; fullscreen; encrypted-media" style={{ width: '100%', height: '100vh', border: '1px solid black' }}></iframe>
                    </Box>
                </div>
            </div>
            </div>
        </div>
        )}
      </header>
    </div>
  );
}

export default App;
