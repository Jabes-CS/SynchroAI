// src/pages/Perfil.jsx
import { useState, useEffect } from 'react';
import { getProfile } from '../api/cliente';

function Perfil() {
  const [perfil, setPerfil] = useState(null);
  const [erro, setErro] = useState('');

  useEffect(() => {
    getProfile()
      .then(data => setPerfil(data))
      .catch(err => setErro(err.message));
  }, []);

  if (erro) return <div className="alert alert-error">{erro}</div>;
  if (!perfil) return <div>Carregando perfil...</div>;

  return (
    <div>
      <h1>Meu Perfil</h1>
      <pre>{JSON.stringify(perfil, null, 2)}</pre>
    </div>
  );
}

export default Perfil;