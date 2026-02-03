export default {
  title: 'पुस्तक प्रबंधन',
  add: 'पुस्तक जोड़ें',
  addNew: 'नई पुस्तक जोड़ें',
  edit: 'पुस्तक संपादित करें',
  searchPlaceholder: 'पुस्तकें खोजें...',
  available: 'उपलब्ध',
  unavailable: 'अनुपलब्ध',
  filterGenre: 'शैली से फ़िल्टर करें',
  filterAuthor: 'लेखक से फ़िल्टर करें',
  availableOnly: 'केवल उपलब्ध',
  currentLanguage: 'वर्तमान भाषा',
  refresh: 'डेटा रीफ्रेश करें',
  refreshing: 'डेटा रीफ्रेश हो रहा है...',

  // Table columns
  columns: {
    title: 'शीर्षक',
    author: 'लेखक',
    genre: 'शैली',
    description: 'विवरण',
    publicationDate: 'प्रकाशन तिथि',
    price: 'कीमत',
    status: 'स्थिति',
    actions: 'क्रियाएँ'
  },

  // Form labels
  form: {
    title: 'शीर्षक',
    author: 'लेखक',
    isbn: 'ISBN',
    genre: 'शैली',
    publicationDate: 'प्रकाशन तिथि',
    pages: 'पृष्ठ',
    price: 'कीमत',
    description: 'विवरण',
    available: 'उपलब्ध'
  },

  // Validation
  validation: {
    titleRequired: 'शीर्षक आवश्यक है',
    authorRequired: 'लेखक आवश्यक है',
    genreRequired: 'शैली आवश्यक है',
    publicationDateRequired: 'प्रकाशन तिथि आवश्यक है',
    pagesRequired: 'पृष्ठ संख्या आवश्यक है',
    pagesMin: 'पृष्ठ संख्या 0 से अधिक होनी चाहिए',
    priceRequired: 'कीमत आवश्यक है',
    priceMin: 'कीमत 0 या अधिक होनी चाहिए'
  },

  // Dialogs
  confirmDelete: 'हटाने की पुष्टि करें',
  confirmDeleteMessage: 'क्या आप वाकई "{title}" को हटाना चाहते हैं?',

  // Notifications
  loadBooksError: 'पुस्तकें लोड करने में विफल',
  loadDataError: 'डेटा लोड करने में विफल',
  loadBookDetailsError: 'पुस्तक विवरण लोड करने में विफल',
  saveError: 'पुस्तक सहेजने में विफल',
  updateSuccess: 'पुस्तक सफलतापूर्वक अद्यतन की गई',
  createSuccess: 'पुस्तक सफलतापूर्वक बनाई गई',
  deleteSuccess: 'पुस्तक सफलतापूर्वक हटाई गई',
  deleteError: 'पुस्तक हटाने में विफल'
}
