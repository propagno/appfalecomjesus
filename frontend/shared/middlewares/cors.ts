/**
 * Configuração CORS para backend
 * 
 * Este arquivo contém as configurações recomendadas para o CORS nos microsserviços
 * permitindo requisições específicas do frontend.
 * 
 * Cada microsserviço deve implementar estas configurações para permitir
 * comunicação segura com o frontend.
 */

// Configuração para Express.js (Node.js)
export const expressCorsMicroservices = {
  origin: [
    'http://localhost:3000', // Frontend local de desenvolvimento
    'https://staging.falecomjesus.com', // Ambiente de staging
    'https://falecomjesus.com' // Ambiente de produção
  ],
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: [
    'Content-Type', 
    'Authorization', 
    'X-Requested-With', 
    'Accept', 
    'Origin', 
    'X-App-Version'
  ],
  credentials: true, // Necessário para cookies HttpOnly
  maxAge: 86400, // Cache de preflight por 24h
  optionsSuccessStatus: 204 // Padrão para solicitações OPTIONS
};

// Configuração para Flask (Python)
export const flaskCorsMicroservices = {
  origins: [
    'http://localhost:3000',
    'https://staging.falecomjesus.com',
    'https://falecomjesus.com'
  ],
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowed_headers: [
    'Content-Type', 
    'Authorization', 
    'X-Requested-With', 
    'Accept', 
    'Origin', 
    'X-App-Version'
  ],
  supports_credentials: true,
  max_age: 86400
};

// Exemplo de uso com Express.js
/* 
import cors from 'cors';
import { expressCorsMicroservices } from './shared/middlewares/cors';

const app = express();
app.use(cors(expressCorsMicroservices));
*/

// Exemplo de uso com Flask
/*
from flask import Flask
from flask_cors import CORS
from config import flaskCorsMicroservices

app = Flask(__name__)
CORS(app, **flaskCorsMicroservices)
*/

// Configuração para Nginx (proxy reverso)
export const nginxCorsConfig = `
# Adicionar ao bloco server ou location em nginx.conf
add_header 'Access-Control-Allow-Origin' 'https://falecomjesus.com';
add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS';
add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization, X-Requested-With, Accept, Origin, X-App-Version';
add_header 'Access-Control-Allow-Credentials' 'true';
add_header 'Access-Control-Max-Age' '86400';

# Tratamento especial para requisições OPTIONS (preflight)
if ($request_method = 'OPTIONS') {
    add_header 'Access-Control-Allow-Origin' 'https://falecomjesus.com';
    add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS';
    add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization, X-Requested-With, Accept, Origin, X-App-Version';
    add_header 'Access-Control-Allow-Credentials' 'true';
    add_header 'Access-Control-Max-Age' '86400';
    add_header 'Content-Type' 'text/plain charset=UTF-8';
    add_header 'Content-Length' '0';
    return 204;
}
`;

export default {
  expressCorsMicroservices,
  flaskCorsMicroservices,
  nginxCorsConfig
}; 