/**
 * Utilitário para gerenciamento de cache local
 * Suporta armazenamento em localStorage (padrão) ou indexedDB
 */

import { FEATURES } from '../constants/config';

// Configurações padrão
const DEFAULT_TTL = 1000 * 60 * 60; // 1 hora em milissegundos
const DEFAULT_PREFIX = 'fcj_cache_';
const DEFAULT_VERSION = 1;
const DEFAULT_DB_NAME = 'FaleComJesusCache';

// Tipos de armazenamento disponíveis
export type StorageType = 'localStorage' | 'indexedDB';

// Configurações para o cache
export interface CacheConfig {
  ttl?: number;              // Tempo de vida em milissegundos
  prefix?: string;           // Prefixo para chaves no localStorage
  storageType?: StorageType; // Tipo de armazenamento
  dbName?: string;           // Nome do banco indexedDB
  dbVersion?: number;        // Versão do banco indexedDB
}

// Interface para os itens do cache
interface CacheItem<T> {
  data: T;
  expiry: number;
}

/**
 * Classe para gerenciar cache local com localStorage ou IndexedDB
 */
export class LocalCache {
  private config: Required<CacheConfig>;
  private db: IDBDatabase | null = null;
  private dbReady: Promise<void> | null = null;

  constructor(config: CacheConfig = {}) {
    // Configura valores padrão
    this.config = {
      ttl: config.ttl ?? DEFAULT_TTL,
      prefix: config.prefix ?? DEFAULT_PREFIX,
      storageType: config.storageType ?? 'localStorage',
      dbName: config.dbName ?? DEFAULT_DB_NAME,
      dbVersion: config.dbVersion ?? DEFAULT_VERSION,
    };

    // Inicializa o IndexedDB se necessário
    if (this.config.storageType === 'indexedDB') {
      this.initIndexedDB();
    }
  }

  /**
   * Inicializa o banco de dados IndexedDB
   */
  private initIndexedDB(): void {
    if (!window.indexedDB) {
      console.warn('IndexedDB não é suportado neste navegador. Usando localStorage como fallback.');
      this.config.storageType = 'localStorage';
      return;
    }

    this.dbReady = new Promise<void>((resolve, reject) => {
      const request = indexedDB.open(this.config.dbName, this.config.dbVersion);

      request.onerror = (event) => {
        console.error('Erro ao abrir IndexedDB:', event);
        this.config.storageType = 'localStorage';
        reject(new Error('Falha ao abrir IndexedDB'));
      };

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;
        
        // Cria o object store se não existir
        if (!db.objectStoreNames.contains('cache')) {
          db.createObjectStore('cache', { keyPath: 'key' });
        }
      };

      request.onsuccess = (event) => {
        this.db = (event.target as IDBOpenDBRequest).result;
        resolve();
      };
    });
  }

  /**
   * Garante que o IndexedDB está pronto antes de executar uma operação
   */
  private async ensureDBReady(): Promise<void> {
    if (this.config.storageType === 'indexedDB' && this.dbReady) {
      await this.dbReady;
    }
  }

  /**
   * Salva um item no cache
   * @param key Chave para identificar o item
   * @param data Dados a serem armazenados
   * @param ttl Tempo de vida opcional (usa o padrão se não informado)
   */
  async set<T>(key: string, data: T, ttl?: number): Promise<void> {
    const actualTtl = ttl ?? this.config.ttl;
    const now = Date.now();
    const expires = now + actualTtl;

    const cacheItem: CacheItem<T> = {
      data,
      expiry: expires,
    };

    if (this.config.storageType === 'localStorage') {
      try {
        localStorage.setItem(
          this.config.prefix + key,
          JSON.stringify(cacheItem)
        );
      } catch (error) {
        console.error('Erro ao salvar no localStorage:', error);
      }
    } else {
      await this.ensureDBReady();
      
      if (!this.db) return;

      return new Promise((resolve, reject) => {
        try {
          const transaction = this.db!.transaction(['cache'], 'readwrite');
          const store = transaction.objectStore('cache');
          
          const request = store.put({
            key,
            ...cacheItem,
          });

          request.onsuccess = () => resolve();
          request.onerror = (event) => reject(event);
        } catch (error) {
          reject(error);
        }
      });
    }
  }

  /**
   * Recupera um item do cache
   * @param key Chave do item a ser recuperado
   * @returns Os dados armazenados ou null se não existir ou estiver expirado
   */
  async get<T>(key: string): Promise<T | null> {
    if (this.config.storageType === 'localStorage') {
      try {
        const item = localStorage.getItem(this.config.prefix + key);
        
        if (!item) {
          return null;
        }
        
        const cacheItem = JSON.parse(item) as CacheItem<T>;
        
        // Verifica se o item expirou
        if (Date.now() > cacheItem.expiry) {
          // Remove itens expirados automaticamente
          this.remove(key);
          return null;
        }
        
        return cacheItem.data;
      } catch (error) {
        console.error('Erro ao recuperar do localStorage:', error);
        return null;
      }
    } else {
      await this.ensureDBReady();
      
      if (!this.db) return null;

      return new Promise((resolve, reject) => {
        try {
          const transaction = this.db!.transaction(['cache'], 'readonly');
          const store = transaction.objectStore('cache');
          const request = store.get(key);

          request.onsuccess = (event) => {
            const result = (event.target as IDBRequest).result;
            
            if (!result) {
              return resolve(null);
            }
            
            // Verifica se o item expirou
            if (Date.now() > result.expiry) {
              // Remove itens expirados automaticamente
              this.remove(key);
              return resolve(null);
            }
            
            resolve(result.data);
          };

          request.onerror = () => resolve(null);
        } catch (error) {
          console.error('Erro ao recuperar do IndexedDB:', error);
          resolve(null);
        }
      });
    }
  }

  /**
   * Remove um item do cache
   * @param key Chave do item a ser removido
   */
  async remove(key: string): Promise<void> {
    if (this.config.storageType === 'localStorage') {
      localStorage.removeItem(this.config.prefix + key);
    } else {
      await this.ensureDBReady();
      
      if (!this.db) return;

      return new Promise((resolve, reject) => {
        try {
          const transaction = this.db!.transaction(['cache'], 'readwrite');
          const store = transaction.objectStore('cache');
          const request = store.delete(key);

          request.onsuccess = () => resolve();
          request.onerror = (event) => reject(event);
        } catch (error) {
          reject(error);
        }
      });
    }
  }

  /**
   * Limpa todos os itens do cache
   */
  async clear(): Promise<void> {
    if (this.config.storageType === 'localStorage') {
      // Remove apenas os itens com o prefixo correto
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key && key.startsWith(this.config.prefix)) {
          localStorage.removeItem(key);
        }
      }
    } else {
      await this.ensureDBReady();
      
      if (!this.db) return;

      return new Promise((resolve, reject) => {
        try {
          const transaction = this.db!.transaction(['cache'], 'readwrite');
          const store = transaction.objectStore('cache');
          const request = store.clear();

          request.onsuccess = () => resolve();
          request.onerror = (event) => reject(event);
        } catch (error) {
          reject(error);
        }
      });
    }
  }

  /**
   * Remove todos os itens expirados do cache
   */
  async clearExpired(): Promise<void> {
    const now = Date.now();

    if (this.config.storageType === 'localStorage') {
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        
        if (key && key.startsWith(this.config.prefix)) {
          try {
            const item = localStorage.getItem(key);
            
            if (item) {
              const cacheItem = JSON.parse(item) as CacheItem<any>;
              
              if (now > cacheItem.expiry) {
                localStorage.removeItem(key);
              }
            }
          } catch (error) {
            // Ignora erros de parsing
          }
        }
      }
    } else {
      await this.ensureDBReady();
      
      if (!this.db) return;

      // No IndexedDB, precisamos ler todos os itens e depois remover os expirados
      return new Promise((resolve, reject) => {
        try {
          const transaction = this.db!.transaction(['cache'], 'readwrite');
          const store = transaction.objectStore('cache');
          const request = store.openCursor();
          
          request.onsuccess = (event) => {
            const cursor = (event.target as IDBRequest).result as IDBCursorWithValue;
            
            if (cursor) {
              const value = cursor.value;
              
              if (now > value.expiry) {
                store.delete(cursor.key);
              }
              
              cursor.continue();
            } else {
              resolve();
            }
          };

          request.onerror = (event) => reject(event);
        } catch (error) {
          reject(error);
        }
      });
    }
  }
}

/**
 * Salva dados no cache local (localStorage ou IndexedDB)
 * @param key Chave para identificar os dados
 * @param data Dados a serem salvos
 * @param ttl Tempo de vida em ms (padrão: 5 minutos)
 */
export function saveToCache<T>(key: string, data: T, ttl = 300000): void {
  try {
    const item: CacheItem<T> = {
      data,
      expiry: Date.now() + ttl,
    };
    
    // Por padrão, usa localStorage para dados simples
    localStorage.setItem(key, JSON.stringify(item));
    
    // TODO: Implementar suporte para IndexedDB quando o tamanho dos dados for grande
    // ou quando FEATURES.advancedCache estiver habilitado
  } catch (error) {
    console.warn('Erro ao salvar no cache:', error);
    // Se falhar (ex: localStorage cheio), tenta remover itens antigos e tentar novamente
    cleanExpiredCache();
  }
}

/**
 * Recupera dados do cache local
 * @param key Chave dos dados
 * @returns Dados recuperados ou null se não encontrado ou expirado
 */
export function getFromCache<T>(key: string): T | null {
  try {
    const itemStr = localStorage.getItem(key);
    
    if (!itemStr) {
      return null;
    }
    
    const item: CacheItem<T> = JSON.parse(itemStr);
    
    // Verifica se o item expirou
    if (Date.now() > item.expiry) {
      localStorage.removeItem(key);
      return null;
    }
    
    return item.data;
  } catch (error) {
    console.warn('Erro ao recuperar do cache:', error);
    return null;
  }
}

/**
 * Remove um item específico do cache
 * @param key Chave do item a ser removido
 */
export function removeFromCache(key: string): void {
  try {
    localStorage.removeItem(key);
  } catch (error) {
    console.warn('Erro ao remover do cache:', error);
  }
}

/**
 * Limpa todo o cache relacionado à aplicação
 * @param prefix Prefixo opcional para limpar apenas itens específicos
 */
export function clearCache(prefix?: string): void {
  try {
    if (prefix) {
      // Remove apenas itens com o prefixo especificado
      Object.keys(localStorage).forEach((key) => {
        if (key.startsWith(prefix)) {
          localStorage.removeItem(key);
        }
      });
    } else {
      // Limpa todo o localStorage (pode afetar outras aplicações)
      // Por isso é recomendado sempre usar um prefixo
      localStorage.clear();
    }
  } catch (error) {
    console.warn('Erro ao limpar cache:', error);
  }
}

/**
 * Remove itens expirados do cache
 */
export function cleanExpiredCache(): void {
  try {
    const now = Date.now();
    
    Object.keys(localStorage).forEach((key) => {
      const itemStr = localStorage.getItem(key);
      
      if (itemStr) {
        try {
          const item = JSON.parse(itemStr);
          
          if (item.expiry && now > item.expiry) {
            localStorage.removeItem(key);
          }
        } catch {
          // Ignora itens que não podem ser parseados como JSON
        }
      }
    });
  } catch (error) {
    console.warn('Erro ao limpar cache expirado:', error);
  }
}

/**
 * Adiciona um item ao cache somente se a feature de cache estiver habilitada
 * @param key Chave para identificar os dados
 * @param data Dados a serem salvos
 * @param ttl Tempo de vida em ms
 */
export function conditionalSaveToCache<T>(key: string, data: T, ttl = 300000): void {
  if (FEATURES.offlineMode) {
    saveToCache(key, data, ttl);
  }
}

/**
 * Inicializa o sistema de cache, removendo itens expirados
 */
export function initCache(): void {
  cleanExpiredCache();
  
  // Configura limpeza periódica de cache (a cada hora)
  setInterval(cleanExpiredCache, 3600000);
}

// Exporta um objeto com todos os métodos
export const cacheUtils = {
  saveToCache,
  getFromCache,
  removeFromCache,
  clearCache,
  cleanExpiredCache,
  initCache,
  LocalCache
}; 