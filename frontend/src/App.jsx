import Copilot from './pages/Copilot';
import './index.css';  // <-- Make sure this line is here to bundle Tailwind styles!
import './App.css';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Copilot />
    </div>
  );
}

export default App;
