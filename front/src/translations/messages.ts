import { en, fr } from 'vuetify/locale'

export default {
    en: {
        $vuetify: {
            ...en
        },
        title: "Ornipedia",
        subtitle: "The bird encyclopedia",

        speciesSelect: "Filter by species",
        search: "Search by name",

        settings: "Settings",
        settingsTheme: "Theme",
        settingsThemeLight: "Light",
        settingsThemeDark: "Dark",
        settingsLanguage: "Language",

        navigation: {
            home: {
                title: "Home",
                desc: "",
            },
            image_gallery: {
                title: "Image gallery",
                desc: "Browse the image gallery"
            } ,
            bird_finder: {
                title:"Bird finder",
                desc:"Search and find a bird"
            } ,
            quiz: {
                title: "Quiz",
                desc: "Test you knowledge!"
            }   
        },

        bird_finder: {
            coming_soon: {
                title: "Coming soon!",
                desc: "This functionality is under development! Stay tuned for more updates!"
            }
        },
        quiz: {
            coming_soon: {
                title: "Coming soon!",
                desc: "Get ready to test your knowledge about birds! Stay tuned for more updates!"
            }
        },
        image_gallery: {
            no_match: {
                title: "Unable to find what you are looking for.",
                desc: "Try to adjust the search terms or filters."
            }
        }
    },
    fr: {
        $vuetify: {
            ...fr
        },
        title: "Ornipedia",
        subtitle: "L'encyclopédie ornithologique",

        speciesSelect: "Filtrer par espèce",
        search: "Recherche par nom",

        settings: "Paramètres",
        settingsTheme: "Thème",
        settingsThemeLight: "Clair",
        settingsThemeDark: "Sombre",
        settingsLanguage: "Langue",

        navigation: {
            home: {
                title: "Home",
                desc: "",
            },
            image_gallery: {
                title: "Galerie d'images",
                desc: "Parcourez la galerie d'images"
            } ,
            bird_finder: {
                title:"Trouver un oiseau",
                desc:"Cherchez et trouver un oiseau"
            } ,
            quiz: {
                title: "Quiz",
                desc: "Testez vos connaissances !"
            }
        },

        bird_finder: {
            coming_soon: {
                title: "Bientôt disponible !",
                desc: "Cette fonctionnalité est en cours de développement ! Restez à l'écoute des nouvelles mises à jour !"
            }
        },
        quiz: {
            coming_soon: {
                title: "Bientôt disponible !",
                desc: "Préparez-vous à tester vos connaissances sur les oiseaux ! Restez à l'écoute des nouvelles mises à jour !"
            }
        },
        image_gallery: {
            no_match: {
                title: "Impossible de trouver une image correspondant à votre recherche",
                desc: "Essayez d'ajuster les critères de recherche ou les filtres."
            }
        }
    },
}
