<template>
  <div>
    <h1>Itens Cadastrados</h1>
  <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Nome</th>
          <th>Descrição</th>
          <th>Valor</th>
          <th class="col-acoes" colspan="3">Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in itens" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.nome }}</td>
          <td>{{ item.descricao }}</td>
          <td>
            {{
              item.valorAtual !== undefined && item.valorAtual !== '-' && item.valorAtual !== 'Erro'
                ? formatarMoeda(item.valorAtual)
                : (item.valorAtual !== undefined ? item.valorAtual : 'Carregando...')
            }}
          </td>
          <td><button class="btn-edit btn-small" @click="editItem(item)" title="Editar"><font-awesome-icon icon="pen" /></button></td>
          <td><button class="btn-delete btn-small" @click="deleteItem(item.id)" title="Deletar"><font-awesome-icon icon="trash" /></button></td>
          <td><button class="btn-value btn-small" @click="editValue(item)" title="Ajuste valor"><font-awesome-icon icon="coins" /></button></td>
        </tr>
      </tbody>
    </table>
    <div class="total-label">
      <strong>Total:</strong>
      {{ formatarMoeda(totalValores) }}
    </div>
    <button @click="showForm = true" style="margin-top:16px;">
      <font-awesome-icon icon="plus" /> Cadastrar Novo Item
    </button>
    <!-- Modal de ajuste de valor -->
    <div v-if="showValueForm" class="modal-bg">
      <div class="modal">
        <h2 class="modal-title">Cadastrar novo valor</h2>
        <form @submit.prevent="saveValue">
          <label>Valor:</label>
          <input v-model.number="valueForm.valor" type="number" min="0" required />
          <div style="margin-top:12px;">
            <button class="btn-value" type="submit">Salvar <font-awesome-icon icon="save" /></button>
            <button class="btn-cancel" type="button" @click="cancelValue">Cancelar <font-awesome-icon icon="ban" /></button>
          </div>
        </form>
      </div>
    </div>
    <div v-if="showForm">
      <h2>{{ editing ? 'Editar' : 'Novo' }} Item</h2>
      <form @submit.prevent="saveItem">
        <input v-model="form.nome" placeholder="Nome" required />
        <input v-model="form.descricao" placeholder="Descrição" required />
        <button class="btn-save" type="submit">Salvar <font-awesome-icon icon="save" /></button>
        <button class="btn-cancel" type="button" @click="cancel">Cancelar <font-awesome-icon icon="ban" /></button>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  data() {
    return {
      itens: [],
      showForm: false,
      editing: false,
      showValueForm: false,
      valueForm: { item_id: null, valor: null },
      form: { id: null, nome: '', descricao: '' },
    };
  },
  computed: {
    totalValores() {
      return this.itens.reduce((acc, item) => {
        if (item.valorAtual !== undefined && item.valorAtual !== '-' && item.valorAtual !== 'Erro') {
          return acc + Number(item.valorAtual);
        }
        return acc;
      }, 0);
    }
  },
  mounted() {
    this.fetchItens();
  },
  methods: {
    editValue(item) {
      this.valueForm = { item_id: item.id, valor: null };
      this.showValueForm = true;
      this.showForm = false;
      this.editing = false;
    },
    async saveValue() {
      try {
        await api.post('/valores/', {
          item_id: this.valueForm.item_id,
          valor: this.valueForm.valor
        });
        this.showValueForm = false;
        this.valueForm = { item_id: null, valor: null };
        this.fetchItens();
      } catch (e) {
        alert('Erro ao salvar valor!');
      }
    },
    cancelValue() {
      this.showValueForm = false;
      this.valueForm = { item_id: null, valor: null };
    },
    formatarMoeda(valor) {
      return Number(valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
    },
    async fetchItens() {
      const res = await api.get('/itens/');
      const itensOrdenados = res.data.sort((a, b) => a.id - b.id);
      // Adiciona campo valorAtual
      this.itens = itensOrdenados.map(item => ({ ...item, valorAtual: undefined }));
      // Busca valor atual para cada item
      for (const item of this.itens) {
        try {
          const valoresRes = await api.get(`/valores/${item.id}`);
          const valores = valoresRes.data;
          if (valores.length > 0) {
            // Ordena por data_cadastro decrescente
            valores.sort((a, b) => new Date(b.data_cadastro) - new Date(a.data_cadastro));
            item.valorAtual = valores[0].valor;
          } else {
            item.valorAtual = '-';
          }
        } catch (e) {
          item.valorAtual = 'Erro';
        }
      }
    },
    async saveItem() {
      if (this.editing) {
        await api.put(`/itens/${this.form.id}`, {
          nome: this.form.nome,
          descricao: this.form.descricao,
        });
      } else {
        await api.post('/itens/', {
          nome: this.form.nome,
          descricao: this.form.descricao,
        });
      }
      this.showForm = false;
      this.editing = false;
      this.form = { id: null, nome: '', descricao: '' };
      this.fetchItens();
    },
    editItem(item) {
      this.form = { ...item };
      this.showForm = true;
      this.editing = true;
    },
    async deleteItem(id) {
        await api.delete(`/itens/${id}`);
        await this.fetchItens();
    },
    cancel() {
      this.showForm = false;
      this.editing = false;
      this.form = { id: null, nome: '', descricao: '' };
    },
  },
};
</script>

<style scoped>
.total-label {
  margin: 16px 0 8px 0;
  font-size: 1.2rem;
  text-align: right;
}
.btn-value {
  background: #22c55e;
}
.btn-value:hover {
  background: #16a34a;
}
/* Modal simples */
.modal-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal {
  background: #fff;
  padding: 24px;
  border-radius: 8px;
  min-width: 300px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.2);
}
.modal-title {
  color: #000;
}
/* Coluna de ações menor */
.col-acoes {
  width: 5%;
  white-space: nowrap;
}
/* Botão pequeno */
.btn-small {
  height: 28px;
  padding: 0 8px;
  font-size: 0.9rem;
}
table {
  width: 700px;
  border-collapse: collapse;
  margin-bottom: 16px;
}
th, td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: center;
}
th {
  background: #f4f4f4;
  color: #000;
}
form { margin-top: 16px; }
input {
  margin-right: 8px;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  height: 38px;
  box-sizing: border-box;
  transition: border-color 0.2s;
}
input:focus {
  border-color: #42b883;
  outline: none;
}
button {
  margin-right: 4px;
  height: 38px;
  padding: 0 16px;
  border-radius: 4px;
  border: none;
  color: #fff;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-save,
button[type="submit"] {
  background: #22c55e;
}
.btn-save:hover,
button[type="submit"]:hover {
  background: #16a34a;
}
.btn-cancel {
  background: #dc2626;
}
.btn-cancel:hover {
  background: #b91c1c;
}
.btn-edit {
  background: #2563eb;
}
.btn-edit:hover {
  background: #1d4ed8;
}
.btn-delete {
  background: #dc2626;
}
.btn-delete:hover {
  background: #b91c1c;
}
</style>
