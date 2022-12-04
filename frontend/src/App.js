import './App.css';
import NavBar from './components/NavBarElem';
import {BrowserRouter as Router} from 'react-router-dom';

function App() {
  return (
    <Router>
      <NavBar />
    </Router>
  );
}

export default App;
