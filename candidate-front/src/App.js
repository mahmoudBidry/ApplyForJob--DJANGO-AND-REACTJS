import './App.css';
import AddCandidate from './component/AddCandidate';
import ViewCandidates from './component/ViewCandidates';
import ViewCandidateDetails from './component/ViewCandidateDetails';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router,  Route, Routes } from "react-router-dom";


function App() {
  return (
    <div className="App" style={{backgroundColor: '#FFFFFF', height: '100vh'}}>
     {/* <AddCandidate /> */}

    <Router>
      <Routes>
        <Route path="/" exact element={<ViewCandidates/>} />
        <Route path="/ViewCandidateDetails/:id" exact element={<ViewCandidateDetails/>} />
        <Route path="/AddCandidate" exact element={<AddCandidate />} />
      </Routes>
    </Router>

    </div>
  );
}

export default App;


export function b64ToBlob (cvString){
  if(cvString){
    const byteCharacters = atob(cvString);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const cvBlob = new Blob([byteArray], { type: 'application/pdf' });
    return URL.createObjectURL(cvBlob)
  }
}