/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html', // Para pegar todos os arquivos HTML nos templates
    './autenticacao/templates/**/*.html', // Para pegar templates específicos do app 'autenticacao'
    './gerenciador_tabelas/templates/**/*.html', // Para pegar templates do app 'gerenciador_tabelas'
    './api_integration/templates/**/*.html', // Para pegar templates do app 'api_integration', se existir
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
