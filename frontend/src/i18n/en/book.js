export default {
  title: 'Books Management',
  add: 'Add Book',
  addNew: 'Add New Book',
  edit: 'Edit Book',
  searchPlaceholder: 'Search books...',
  available: 'Available',
  unavailable: 'Unavailable',
  filterGenre: 'Filter by Genre',
  filterAuthor: 'Filter by Author',
  availableOnly: 'Available Only',
  currentLanguage: 'Current Language',
  refresh: 'Refresh Data',
  refreshing: 'Refreshing data...',

  // Table columns
  columns: {
    title: 'Title',
    author: 'Author',
    genre: 'Genre',
    description: 'Description',
    publicationDate: 'Publication Date',
    price: 'Price',
    status: 'Status',
    actions: 'Actions'
  },

  // Form labels
  form: {
    title: 'Title',
    author: 'Author',
    isbn: 'ISBN',
    genre: 'Genre',
    publicationDate: 'Publication Date',
    pages: 'Pages',
    price: 'Price',
    description: 'Description',
    available: 'Available'
  },

  // Validation
  validation: {
    titleRequired: 'Title is required',
    authorRequired: 'Author is required',
    genreRequired: 'Genre is required',
    publicationDateRequired: 'Publication date is required',
    pagesRequired: 'Pages is required',
    pagesMin: 'Pages must be greater than 0',
    priceRequired: 'Price is required',
    priceMin: 'Price must be 0 or greater'
  },

  // Dialogs
  confirmDelete: 'Confirm Delete',
  confirmDeleteMessage: 'Are you sure you want to delete "{title}"?',

  // Notifications
  loadBooksError: 'Failed to load books',
  loadDataError: 'Failed to load data',
  loadBookDetailsError: 'Failed to load book details',
  saveError: 'Failed to save book',
  updateSuccess: 'Book updated successfully',
  createSuccess: 'Book created successfully',
  deleteSuccess: 'Book deleted successfully',
  deleteError: 'Failed to delete book'
}
