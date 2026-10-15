// Entries of the navigation (app bar on desktop, drawer on mobile).
// `soon` entries are shown but disabled until the functionality is available.
export const navigationItems = [
    { to: "/", title: "navigation.home.title", icon: "mdi-home-outline", soon: false },
    { to: "/birds", title: "navigation.image_gallery.title", icon: "mdi-image-multiple-outline", soon: false },
    { to: "/bird-finder", title: "navigation.bird_finder.title", icon: "mdi-magnify-expand", soon: true },
    { to: "/quiz", title: "navigation.quiz.title", icon: "mdi-chat-question-outline", soon: true },
]
