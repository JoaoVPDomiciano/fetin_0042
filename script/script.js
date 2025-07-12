const { createClient } = window.supabase;

const SUPABASE_URL = 'https://epruvcgigotpcptjaqyr.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVwcnV2Y2dpZ290cGNwdGphcXlyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY5NjM3MTMsImV4cCI6MjA2MjUzOTcxM30.T-wYUDATWI9Iw-UXNDyjI7aCN5EF3306inlhlIDFGbs';

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

let paginaLogs = 1;
let paginaSpeed = 1;
let paginaTrafego = 1;

const itensPorPagina = 10;

async function carregarLogs(pagina = 1) {
  const inicio = (pagina - 1) * itensPorPagina;
  const fim = inicio + itensPorPagina - 1;

  const { data, error } = await supabase
    .from('logs')
    .select('*')
    .order('timestamp', { ascending: false })
    .range(inicio, fim);

  if (error) {
    console.error('Erro ao carregar logs:', error);
    return;
  }

  atualizarTabelaLogs(data);
}

async function carregarSpeedtest(pagina = 1) {
  const inicio = (pagina - 1) * itensPorPagina;
  const fim = inicio + itensPorPagina - 1;

  const { data, error } = await supabase
    .from('speedtest')
    .select('*')
    .order('timestamp', { ascending: false })
    .range(inicio, fim);

  if (error) {
    console.error('Erro ao carregar speedtest:', error);
    return;
  }

  atualizarTabelaSpeedtest(data);
}
async function carregarTrafego(pagina = 1) {
  const inicio = (pagina - 1) * itensPorPagina;
  const fim = inicio + itensPorPagina - 1;

  const { data, error } = await supabase
    .from('trafego')
    .select('*')
    .order('timestamp', { ascending: false })
    .range(inicio, fim);

  if (error) {
    console.error('Erro ao carregar Trafego:', error);
    return;
  }

  atualizarTabelaTrafego(data);
}

function atualizarTabelaLogs(dados) {
  const tbody = document.getElementById('dados-tabela-logs');
  tbody.innerHTML = '';

  dados.forEach((dado) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${formatarData(dado.timestamp)}</td>
      <td>${dado.id}</td>
      <td>${dado.mensagem}</td>
      <td>${dado.nivel}</td>
      <td>${dado.origem}</td>
      <td>${dado.evento_id}</td>
    `;
    tbody.appendChild(row);
  });
}

function atualizarTabelaSpeedtest(dados) {
  const tbody = document.getElementById('dados-tabela-speedtest');
  tbody.innerHTML = '';

  dados.forEach((dado) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${formatarData(dado.timestamp)}</td>
      <td>${dado.ping}</td>
      <td>${dado.download} Mbps</td>
      <td>${dado.upload} Mbps</td>
    `;
    tbody.appendChild(row);
  });
}

function atualizarTabelaTrafego(dados) {
  const tbody = document.getElementById('dados-tabela-trafego');
  tbody.innerHTML = '';

  dados.forEach((dado) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${formatarData(dado.timestamp)}</td>
      <td>${dado.id}</td>
      <td>${dado.porta} </td>
      <td>${dado.tipo} </td>
    `;
    tbody.appendChild(row);
  });
}

function formatarData(dataISO) {
  const data = new Date(dataISO);
  return data.toLocaleString();
}

window.proximaPaginaLogs = () => {
  paginaLogs++;
  carregarLogs(paginaLogs);
};
window.paginaAnteriorLogs = () => {
  if (paginaLogs > 1) {
    paginaLogs--;
    carregarLogs(paginaLogs);
  }
};

window.proximaPaginaSpeed = () => {
  paginaSpeed++;
  carregarSpeedtest(paginaSpeed);
};
window.paginaAnteriorSpeed = () => {
  if (paginaSpeed > 1) {
    paginaSpeed--;
    carregarSpeedtest(paginaSpeed);
  }
};

window.proximaPaginaTrafego = () => {
  paginaTrafego++;
  carregarTrafego(paginaTrafego);
};
window.paginaAnteriorTrafego = () => {
  if (paginaTrafego > 1) {
    paginaTrafego--;
    carregarTrafego(paginaTrafego);
  }
};

window.mostrarTabela = (id) => {
  document.getElementById('logs').classList.remove('ativo');
  document.getElementById('speedtest').classList.remove('ativo');
  document.getElementById('trafego').classList.remove('ativo');

  if (id === 'logs') {
    carregarLogs();
  } else if (id === 'speedtest') {
    carregarSpeedtest();
  }
    else if (id === 'trafego') {
    carregarTrafego();
  }

  document.getElementById(id).classList.add('ativo');
};
