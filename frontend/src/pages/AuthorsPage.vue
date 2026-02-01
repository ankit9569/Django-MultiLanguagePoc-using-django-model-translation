<template>
  <q-page class="q-pa-md">
    <div class="row q-mb-md">
      <div class="col">
        <h4>Authors Management</h4>
      </div>
      <div class="col-auto">
        <q-btn 
          color="primary" 
          icon="add" 
          label="Add Author"
          @click="showAddDialog = true"
        />
      </div>
    </div>

    <!-- Search and Filters -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="row q-gutter-md">
          <div class="col-12 col-md-6">
            <q-input
              v-model="searchQuery"
              placeholder="Search authors..."
              outlined
              dense
              clearable
              @update:model-value="onSearch"
            >
              <template v-slot:prepend>
                <q-icon name="search" />
              </template>
            </q-input>
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Authors Table -->
    <q-table
      :rows="authors"
      :columns="columns"
      :loading="loading"
      row-key="id"
      :pagination="{ rowsPerPage: 10 }"
    >
      <template v-slot:body-cell-actions="props">
        <q-td :props="props">
          <q-btn 
            flat 
            round 
            color="primary" 
            icon="edit"
            size="sm"
            @click="editAuthor(props.row)"
          />
          <q-btn 
            flat 
            round 
            color="negative" 
            icon="delete"
            size="sm"
            @click="confirmDelete(props.row)"
          />
          <q-btn 
            flat 
            round 
            color="info" 
            icon="book"
            size="sm"
            @click="viewBooks(props.row)"
          />
        </q-td>
      </template>
    </q-table>

    <!-- Add/Edit Author Dialog -->
    <q-dialog v-model="showAddDialog" persistent>
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">{{ editingAuthor ? 'Edit Author' : 'Add New Author' }}</div>
        </q-card-section>

        <q-card-section>
          <q-form @submit="saveAuthor" class="q-gutter-md">
            <q-input
              v-model="authorForm.first_name"
              label="First Name"
              outlined
              :rules="[val => !!val || 'First name is required']"
            />
            
            <q-input
              v-model="authorForm.last_name"
              label="Last Name"
              outlined
              :rules="[val => !!val || 'Last name is required']"
            />
            
            <q-input
              v-model="authorForm.email"
              label="Email"
              type="email"
              outlined
              :rules="[
                val => !!val || 'Email is required',
                val => /.+@.+\..+/.test(val) || 'Please enter a valid email'
              ]"
            />
            
            <q-input
              v-model="authorForm.birth_date"
              label="Birth Date"
              type="date"
              outlined
            />
            
            <q-input
              v-model="authorForm.bio"
              label="Biography"
              type="textarea"
              outlined
              rows="3"
            />
          </q-form>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" @click="closeDialog" />
          <q-btn 
            color="primary" 
            label="Save" 
            @click="saveAuthor"
            :loading="loading"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Author Books Dialog -->
    <q-dialog v-model="showBooksDialog">
      <q-card style="min-width: 600px">
        <q-card-section>
          <div class="text-h6">Books by {{ selectedAuthor?.full_name }}</div>
        </q-card-section>

        <q-card-section>
          <q-list v-if="authorBooks.length > 0">
            <q-item v-for="book in authorBooks" :key="book.id">
              <q-item-section>
                <q-item-label>{{ book.title }}</q-item-label>
                <q-item-label caption>{{ book.genre }} - ${{ book.price }}</q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-chip 
                  :color="book.is_available ? 'positive' : 'negative'"
                  text-color="white"
                  size="sm"
                >
                  {{ book.is_available ? 'Available' : 'Unavailable' }}
                </q-chip>
              </q-item-section>
            </q-item>
          </q-list>
          <div v-else class="text-center text-grey-6">
            No books found for this author.
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Close" @click="showBooksDialog = false" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>


<script>
import { api } from 'src/boot/axios'

export default {
  name: 'AuthorsPage',

  data () {
    return {
      authors: [],
      loading: false,
      showAddDialog: false,
      showBooksDialog: false,
      editingAuthor: null,
      selectedAuthor: null,
      authorBooks: [],
      searchQuery: '',

      authorForm: {
        first_name: '',
        last_name: '',
        email: '',
        birth_date: '',
        bio: ''
      },

      columns: [
        {
          name: 'full_name',
          required: true,
          label: 'Name',
          align: 'left',
          field: 'full_name',
          sortable: true
        },
        {
          name: 'email',
          label: 'Email',
          align: 'left',
          field: 'email',
          sortable: true
        },
        {
          name: 'books_count',
          label: 'Books',
          align: 'center',
          field: 'books_count',
          sortable: true
        },
        {
          name: 'actions',
          label: 'Actions',
          align: 'center'
        }
      ]
    }
  },

  mounted () {
    this.loadAuthors()
  },

  methods: {
    async loadAuthors (params = {}) {
      this.loading = true
      try {
        const response = await api.get('authors/', { params })
        this.authors = response.data.results || response.data
      } catch (error) {
        this.$q.notify({
          type: 'negative',
          message: 'Failed to load authors'
        })
      } finally {
        this.loading = false
      }
    },

    onSearch () {
      this.loadAuthors({ search: this.searchQuery })
    },

    editAuthor (author) {
      this.editingAuthor = author
      this.authorForm = { ...author }
      this.showAddDialog = true
    },

    async saveAuthor () {
      this.loading = true
      try {
        if (this.editingAuthor) {
          const response = await api.put(
            `authors/${this.editingAuthor.id}/`,
            this.authorForm
          )

          const index = this.authors.findIndex(
            a => a.id === this.editingAuthor.id
          )
          if (index !== -1) {
            this.authors.splice(index, 1, response.data)
          }

          this.$q.notify({
            type: 'positive',
            message: 'Author updated successfully'
          })
        } else {
          const response = await api.post('authors/', this.authorForm)
          this.authors.unshift(response.data)

          this.$q.notify({
            type: 'positive',
            message: 'Author created successfully'
          })
        }

        this.closeDialog()
      } catch (error) {
        this.$q.notify({
          type: 'negative',
          message:
            error.response?.data?.email?.[0] ||
            'Failed to save author'
        })
      } finally {
        this.loading = false
      }
    },

    confirmDelete (author) {
      this.$q.dialog({
        title: 'Confirm Delete',
        message: `Are you sure you want to delete ${author.full_name}?`,
        cancel: true,
        persistent: true
      }).onOk(async () => {
        this.loading = true
        try {
          await api.delete(`authors/${author.id}/`)
          this.authors = this.authors.filter(a => a.id !== author.id)

          this.$q.notify({
            type: 'positive',
            message: 'Author deleted successfully'
          })
        } catch (error) {
          this.$q.notify({
            type: 'negative',
            message:
              error.response?.data?.error ||
              'Failed to delete author'
          })
        } finally {
          this.loading = false
        }
      })
    },

    async viewBooks (author) {
      this.selectedAuthor = author
      try {
        const response = await api.get(
          `authors/${author.id}/books/`
        )
        this.authorBooks = response.data
        this.showBooksDialog = true
      } catch (error) {
        this.$q.notify({
          type: 'negative',
          message: 'Failed to load author books'
        })
      }
    },

    closeDialog () {
      this.showAddDialog = false
      this.editingAuthor = null
      this.authorForm = {
        first_name: '',
        last_name: '',
        email: '',
        birth_date: '',
        bio: ''
      }
    }
  }
}
</script>
