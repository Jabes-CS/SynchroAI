import Navbar from './components/Navbar'
import Footer from './components/Footer'
import Home from './pages/Home'
import Perfil from './pages/Perfil';

function App() {
  return (
    <div className="bg-gray-50">
      <Navbar />
      <main>
        <Home />
        <Perfil />
      </main>
      <Footer />
    </div>
  )
}

export default App