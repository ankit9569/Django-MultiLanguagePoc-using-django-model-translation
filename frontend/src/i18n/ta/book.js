export default {
  title: 'புத்தக மேலாண்மை',
  add: 'புத்தகம் சேர்க்கவும்',
  addNew: 'புதிய புத்தகம் சேர்க்கவும்',
  edit: 'புத்தகத்தை திருத்தவும்',
  searchPlaceholder: 'புத்தகங்களை தேடுங்கள்...',
  available: 'கிடைக்கிறது',
  unavailable: 'கிடைக்கவில்லை',
  filterGenre: 'வகை மூலம் வடிகட்டவும்',
  filterAuthor: 'ஆசிரியர் மூலம் வடிகட்டவும்',
  availableOnly: 'கிடைக்கும் புத்தகங்கள் மட்டும்',

  // Table columns
  columns: {
    title: 'தலைப்பு',
    author: 'ஆசிரியர்',
    genre: 'வகை',
    description: 'விளக்கம்',
    publicationDate: 'வெளியீட்டு தேதி',
    price: 'விலை',
    status: 'நிலை',
    actions: 'செயல்கள்'
  },

  // Form labels
  form: {
    title: 'தலைப்பு',
    author: 'ஆசிரியர்',
    isbn: 'ISBN',
    genre: 'வகை',
    publicationDate: 'வெளியீட்டு தேதி',
    pages: 'பக்கங்கள்',
    price: 'விலை',
    description: 'விளக்கம்',
    available: 'கிடைக்கிறது'
  },

  // Validation
  validation: {
    titleRequired: 'தலைப்பு அவசியம்',
    authorRequired: 'ஆசிரியர் அவசியம்',
    genreRequired: 'வகை அவசியம்',
    publicationDateRequired: 'வெளியீட்டு தேதி அவசியம்',
    pagesRequired: 'பக்கங்களின் எண்ணிக்கை அவசியம்',
    pagesMin: 'பக்கங்கள் 0-ஐ விட அதிகமாக இருக்க வேண்டும்',
    priceRequired: 'விலை அவசியம்',
    priceMin: 'விலை 0 அல்லது அதற்கு மேல் இருக்க வேண்டும்'
  },

  // Dialogs
  confirmDelete: 'அழிப்பை உறுதிப்படுத்தவும்',
  confirmDeleteMessage: '"{title}" புத்தகத்தை நீக்க வேண்டுமா?',

  // Notifications
  loadBooksError: 'புத்தகங்களை ஏற்றுவதில் தோல்வி',
  loadDataError: 'தகவலை ஏற்றுவதில் தோல்வி',
  loadBookDetailsError: 'புத்தக விவரங்களை ஏற்ற முடியவில்லை',
  saveError: 'புத்தகத்தை சேமிக்க முடியவில்லை',
  updateSuccess: 'புத்தகம் வெற்றிகரமாக புதுப்பிக்கப்பட்டது',
  createSuccess: 'புத்தகம் வெற்றிகரமாக உருவாக்கப்பட்டது',
  deleteSuccess: 'புத்தகம் வெற்றிகரமாக நீக்கப்பட்டது',
  deleteError: 'புத்தகத்தை நீக்க முடியவில்லை'
}
