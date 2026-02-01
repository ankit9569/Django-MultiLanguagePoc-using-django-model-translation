<template>
  <q-page class="q-pa-md">
    <div class="row q-mb-md">
      <div class="col">
        <h4>{{ $t('books.title') }}</h4>
      </div>
      <div class="col-auto">
        <q-btn 
          color="primary" 
          icon="add" 
          :label="$t('books.add')"
          @click="showAddDialog = true"
        />
      </div>
    </div>

    <!-- Search and Filters -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="row q-gutter-md">
          <div class="col-12 col-md-4">
            <q-input
              v-model="searchQuery"
              :placeholder="$t('books.searchPlaceholder')"
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
          
          <div class="col-12 col-md-3">
            <q-select
              v-model="selectedGenre"
              :options="genreOptions"
              option-value="value"
              option-label="label"
              emit-value
              map-options
              :label="$t('books.filterGenre')"
              outlined
              dense
              clearable
              @update:model-value="onFilter"
            />
          </div>
          
          <div class="col-12 col-md-3">
            <q-select
              v-model="selectedAuthor"
              :options="authorsForSelect"
              option-value="value"
              option-label="label"
              emit-value
              map-options
              :label="$t('books.filterAuthor')"
              outlined
              dense
              clearable
              @update:model-value="onFilter"
            />
          </div>
          
          <div class="col-12 col-md-2">
            <q-toggle
              v-model="availableOnly"
              :label="$t('books.availableOnly')"
              @update:model-value="onFilter"
            />
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Books Table -->
    <q-table
      :rows="books"
      :columns="columns"
      :loading="loading"
      row-key="id"
      :pagination="{ rowsPerPage: 10 }"
    >
      <template v-slot:body-cell-is_available="props">
        <q-td :props="props">
          <q-chip 
            :color="props.value ? 'positive' : 'negative'"
            text-color="white"
            size="sm"
          >
            {{ props.value ? $t('books.available') : $t('books.unavailable') }}
          </q-chip>
        </q-td>
      </template>

      <template v-slot:body-cell-price="props">
        <q-td :props="props">
          {{ props.value }}
        </q-td>
      </template>

      <template v-slot:body-cell-actions="props">
        <q-td :props="props">
          <q-btn 
            flat 
            round 
            color="primary" 
            icon="edit"
            size="sm"
            @click="editBook(props.row)"
          />
          <q-btn 
            flat 
            round 
            color="negative" 
            icon="delete"
            size="sm"
            @click="confirmDelete(props.row)"
          />
        </q-td>
      </template>
    </q-table>

    <!-- Add/Edit Book Dialog -->
    <q-dialog v-model="showAddDialog" persistent>
      <q-card style="min-width: 500px">
        <q-card-section>
          <div class="text-h6">{{ editingBook ? $t('books.edit') : $t('books.addNew') }}</div>
        </q-card-section>

        <q-card-section>
          <q-form @submit="saveBook" class="q-gutter-md">
            <q-input
              v-model="bookForm.title"
              :label="$t('books.form.title')"
              outlined
              :rules="[val => !!val || $t('books.validation.titleRequired')]"
            />
            
            <q-select
              v-model="bookForm.author"
              :options="authorsForSelect"
              option-value="value"
              option-label="label"
              emit-value
              map-options
              :label="$t('books.form.author')"
              outlined
              :rules="[val => !!val || $t('books.validation.authorRequired')]"
            />
            
            <q-input
              v-model="bookForm.isbn"
              :label="$t('books.form.isbn')"
              outlined
            />
            
            
            <q-select
              v-model="bookForm.genre"
              :options="genreOptions"
              option-value="value"
              option-label="label"
              emit-value
              map-options
              :label="$t('books.form.genre')"
              outlined
              :rules="[val => !!val || $t('books.validation.genreRequired')]"
            />
            
            <q-input
              v-model="bookForm.publication_date"
              :label="$t('books.form.publicationDate')"
              type="date"
              outlined
              :rules="[val => !!val || $t('books.validation.publicationDateRequired')]"
            />
            
            <div class="row q-gutter-md">
              <div class="col">
                <q-input
                  v-model.number="bookForm.pages"
                  :label="$t('books.form.pages')"
                  type="number"
                  outlined
                  :rules="[
                    val => !!val || $t('books.validation.pagesRequired'),
                    val => val > 0 || $t('books.validation.pagesMin')
                  ]"
                />
              </div>
              
              <div class="col">
                <q-input
                  v-model.number="bookForm.price"
                  :label="$t('books.form.price')"
                  type="number"
                  step="0.01"
                  outlined
                  :rules="[
                    val => val !== null && val !== undefined || $t('books.validation.priceRequired'),
                    val => val >= 0 || $t('books.validation.priceMin')
                  ]"
                />
              </div>
            </div>
            
            <q-input
              v-model="bookForm.description"
              :label="$t('books.form.description')"
              type="textarea"
              outlined
              rows="3"
            />
            
            <q-toggle
              v-model="bookForm.is_available"
              :label="$t('books.form.available')"
            />
          </q-form>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat :label="$t('common.cancel')" @click="closeDialog" />
          <q-btn 
            color="primary" 
            :label="$t('common.save')" 
            @click="saveBook"
            :loading="loading"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>


<script>
import { api } from 'src/boot/axios'

export default {
  name: 'BooksPage',

  data () {
    return {
      books: [],
      authors: [],
      genres: [],
      loading: false,
      showAddDialog: false,
      editingBook: null,

      searchQuery: '',
      selectedGenre: null,
      selectedAuthor: null,
      availableOnly: false,

      bookForm: {
        title: '',
        author: null,
        isbn: '',
        genre: '',
        publication_date: '',
        pages: null,
        price: null,
        description: '',
        is_available: true
      }
    }
  },

  computed: {
    columns () {
      return [
        { name: 'title', required: true, label: this.$t('books.columns.title'), align: 'left', field: 'title', sortable: true },
        { name: 'author_name', label: this.$t('books.columns.author'), align: 'left', field: 'author_name', sortable: true },
        { name: 'genre', label: this.$t('books.columns.genre'), align: 'left', field: 'genre', sortable: true },
        { name: 'description', label: this.$t('books.columns.description'), align: 'left', field: 'description', sortable: true },
        { name: 'publication_date', label: this.$t('books.columns.publicationDate'), align: 'left', field: 'publication_date', sortable: true },
        { name: 'price', label: this.$t('books.columns.price'), align: 'right', field: 'price', sortable: true },
        { name: 'is_available', label: this.$t('books.columns.status'), align: 'center', field: 'is_available' },
        { name: 'actions', label: this.$t('books.columns.actions'), align: 'center' }
      ]
    },

    genreOptions () {
      return this.genres
    },

    authorsForSelect () {
      return this.authors.map(author => ({
        label: author.full_name,
        value: author.id
      }))
    }
  },

  methods: {
    async loadBooks (params = {}) {
      this.loading = true
      try {
        const response = await api.get('books/', { params })
        this.books = response.data.results || response.data
      } catch (error) {
        this.$q.notify({ type: 'negative', message: this.$t('books.loadBooksError') })
      } finally {
        this.loading = false
      }
    },

    async loadData () {
      try {
        const [genresResponse, authorsResponse] = await Promise.all([
          api.get('books/genres/'),
          api.get('authors/')
        ])
        this.genres = genresResponse.data
        this.authors = authorsResponse.data.results || authorsResponse.data
        await this.loadBooks()
      } catch (error) {
        this.$q.notify({ type: 'negative', message: this.$t('books.loadDataError') })
      }
    },

    async onSearch () {
      await this.applyFilters()
    },

    async onFilter () {
      await this.applyFilters()
    },

    async applyFilters () {
      const params = {}
      if (this.searchQuery) params.search = this.searchQuery
      if (this.selectedGenre) params.genre = this.selectedGenre
      if (this.selectedAuthor) params.author = this.selectedAuthor
      if (this.availableOnly) params.available = 'true'
      await this.loadBooks(params)
    },

    async editBook (book) {
      this.loading = true
      try {
        const response = await api.get(`books/${book.id}/`)
        const fullBook = response.data

        this.editingBook = fullBook
        this.bookForm = {
          title: fullBook.title,
          author: fullBook.author,
          isbn: fullBook.isbn || '',
          genre: fullBook.genre,
          publication_date: fullBook.publication_date,
          pages: fullBook.pages,
          price: fullBook.price,
          description: fullBook.description || '',
          is_available: fullBook.is_available
        }

        this.showAddDialog = true
      } catch (error) {
        this.$q.notify({ type: 'negative', message: this.$t('books.loadBookDetailsError') })
      } finally {
        this.loading = false
      }
    },

    async saveBook () {
      this.loading = true
      try {
        const payload = {
          title: this.bookForm.title,
          author: this.bookForm.author,
          isbn: this.bookForm.isbn || null,
          genre: this.bookForm.genre,
          publication_date: this.bookForm.publication_date,
          pages: this.bookForm.pages,
          price: this.bookForm.price,
          description: this.bookForm.description || null,
          is_available: this.bookForm.is_available
        }

        if (this.editingBook) {
          const response = await api.put(`books/${this.editingBook.id}/`, payload)
          const index = this.books.findIndex(b => b.id === this.editingBook.id)

          const listData = {
            id: response.data.id,
            title: response.data.title,
            author: response.data.author,
            author_name: response.data.author_name,
            genre: response.data.genre,
            publication_date: response.data.publication_date,
            price: response.data.price,
            is_available: response.data.is_available
          }

          if (index !== -1) {
            this.books.splice(index, 1, listData)
          } else {
            this.books.unshift(listData)
          }

          this.$q.notify({ type: 'positive', message: this.$t('books.updateSuccess') })
        } else {
          const response = await api.post('books/', payload)
          this.books.unshift({
            id: response.data.id,
            title: response.data.title,
            author: response.data.author,
            author_name: response.data.author_name,
            genre: response.data.genre,
            publication_date: response.data.publication_date,
            price: response.data.price,
            is_available: response.data.is_available
          })

          this.$q.notify({ type: 'positive', message: this.$t('books.createSuccess') })
        }

        this.closeDialog()
      } catch (error) {
        const errMsg =
          error.response?.data?.isbn?.[0] ||
          error.response?.data?.title?.[0] ||
          Object.values(error.response?.data || {}).flat().find(Boolean) ||
          this.$t('books.saveError')

        this.$q.notify({ type: 'negative', message: errMsg })
      } finally {
        this.loading = false
      }
    },

    confirmDelete (book) {
      this.$q.dialog({
        title: this.$t('books.confirmDelete'),
        message: this.$t('books.confirmDeleteMessage', { title: book.title }),
        cancel: true,
        persistent: true
      }).onOk(async () => {
        this.loading = true
        try {
          await api.delete(`books/${book.id}/`)
          this.books = this.books.filter(b => b.id !== book.id)
          this.$q.notify({ type: 'positive', message: this.$t('books.deleteSuccess') })
        } catch (error) {
          this.$q.notify({ type: 'negative', message: this.$t('books.deleteError') })
        } finally {
          this.loading = false
        }
      })
    },

    closeDialog () {
      this.showAddDialog = false
      this.editingBook = null
      this.bookForm = {
        title: '',
        author: null,
        isbn: '',
        genre: '',
        publication_date: '',
        pages: null,
        price: null,
        description: '',
        is_available: true
      }
    }
  },

  mounted () {
    this.loadData()
  }
}
</script>
