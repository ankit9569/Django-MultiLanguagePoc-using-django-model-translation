<template>
  <q-page class="row items-center justify-evenly">
    <div class="full-width q-pa-md">
      <div class="row q-gutter-md">
        <!-- Statistics Cards -->
        <div class="col-12">
          <h4 class="q-mb-md">Dashboard</h4>
        </div>
        
        <div class="col-12 col-md-3">
          <q-card class="bg-primary text-white">
            <q-card-section>
              <div class="text-h6">Total Authors</div>
              <div class="text-h4">{{ statistics.totalAuthors }}</div>
            </q-card-section>
          </q-card>
        </div>

        <div class="col-12 col-md-3">
          <q-card class="bg-secondary text-white">
            <q-card-section>
              <div class="text-h6">Total Books</div>
              <div class="text-h4">{{ statistics.totalBooks }}</div>
            </q-card-section>
          </q-card>
        </div>

        <div class="col-12 col-md-3">
          <q-card class="bg-positive text-white">
            <q-card-section>
              <div class="text-h6">Available Books</div>
              <div class="text-h4">{{ statistics.availableBooks }}</div>
            </q-card-section>
          </q-card>
        </div>

        <div class="col-12 col-md-3">
          <q-card class="bg-warning text-white">
            <q-card-section>
              <div class="text-h6">Unavailable Books</div>
              <div class="text-h4">{{ statistics.unavailableBooks }}</div>
            </q-card-section>
          </q-card>
        </div>

        <!-- Recent Books -->
        <div class="col-12 col-md-6">
          <q-card>
            <q-card-section>
              <div class="text-h6">Recent Books</div>
            </q-card-section>
            <q-card-section>
              <q-list>
                <q-item v-for="book in recentBooks" :key="book.id">
                  <q-item-section>
                    <q-item-label>{{ book.title }}</q-item-label>
                    <q-item-label caption>by {{ book.author_name }}</q-item-label>
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
            </q-card-section>
          </q-card>
        </div>

        <!-- Genre Distribution -->
        <div class="col-12 col-md-6">
          <q-card>
            <q-card-section>
              <div class="text-h6">Genre Distribution</div>
            </q-card-section>
            <q-card-section>
              <div v-for="(count, genre) in statistics.genresDistribution" :key="genre" class="q-mb-sm">
                <div class="row items-center">
                  <div class="col">{{ genre }}</div>
                  <div class="col-auto">
                    <q-chip color="primary" text-color="white" size="sm">
                      {{ count }}
                    </q-chip>
                  </div>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>

        <!-- Quick Actions -->
        <div class="col-12">
          <q-card>
            <q-card-section>
              <div class="text-h6">Quick Actions</div>
            </q-card-section>
            <q-card-section>
              <div class="row q-gutter-md">
                <q-btn 
                  color="primary" 
                  icon="person_add" 
                  label="Add Author"
                  @click="$router.push('/authors')"
                />
                <q-btn 
                  color="secondary" 
                  icon="add" 
                  label="Add Book"
                  @click="$router.push('/books')"
                />
                <q-btn 
                  color="info" 
                  icon="refresh" 
                  label="Refresh Data"
                  @click="loadData"
                  :loading="loading"
                />
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue'
import { api } from 'src/boot/axios'

export default defineComponent({
  name: 'IndexPage',
  
  setup() {
    const loading = ref(false)
    const statistics = ref({
      totalAuthors: 0,
      totalBooks: 0,
      availableBooks: 0,
      unavailableBooks: 0,
      genresDistribution: {}
    })
    
    const recentBooks = ref([])

    const loadData = async () => {
      loading.value = true
      try {
        const [authorsResponse, booksResponse, statsResponse] = await Promise.all([
          api.get('authors/'),
          api.get('books/', { params: { page_size: 5 } }),
          api.get('books/statistics/')
        ])

        const authors = authorsResponse.data.results || authorsResponse.data
        const books = booksResponse.data.results || booksResponse.data
        const stats = statsResponse.data

        statistics.value = {
          totalAuthors: stats.total_authors ?? authors.length,
          totalBooks: stats.total_books ?? 0,
          availableBooks: stats.available_books ?? 0,
          unavailableBooks: stats.unavailable_books ?? 0,
          genresDistribution: stats.genres_distribution ?? {}
        }

        recentBooks.value = books
      } catch (error) {
        console.error('Failed to load dashboard data:', error)
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      loadData()
    })

    return {
      loading,
      statistics,
      recentBooks,
      loadData
    }
  }
})
</script>