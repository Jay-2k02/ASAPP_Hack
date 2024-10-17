import './App.css';
import HomePage from './Components/Homepage/Content';
import Chatpage from './Pages/Chatpage';
import { Route, Routes, useNavigate } from 'react-router-dom';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route exact path='/' element={<HomePage/>}/>
        <Route exact path='/chat' element={<Chatpage/>}/>
      </Routes>
    </div>
  );
}

export default App;
