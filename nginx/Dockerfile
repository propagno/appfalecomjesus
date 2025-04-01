FROM nginx:alpine

# Remover configuração padrão
RUN rm /etc/nginx/conf.d/default.conf

# Criar diretórios de log e cache
RUN mkdir -p /var/log/nginx && \
    touch /var/log/nginx/access.log && \
    touch /var/log/nginx/error.log && \
    touch /var/log/nginx/health_check_access.log && \
    touch /var/log/nginx/health_check_error.log && \
    mkdir -p /var/cache/nginx/client_temp && \
    mkdir -p /var/cache/nginx/proxy_temp && \
    mkdir -p /var/cache/nginx/fastcgi_temp && \
    mkdir -p /var/cache/nginx/uwsgi_temp && \
    mkdir -p /var/cache/nginx/scgi_temp && \
    mkdir -p /var/run && \
    touch /var/run/nginx.pid

# Ajustar permissões
RUN chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/run/nginx.pid

# Usar usuário não-root
USER nginx

# Expor porta
EXPOSE 80

# Comando para iniciar o NGINX
CMD ["nginx", "-g", "daemon off;"] 