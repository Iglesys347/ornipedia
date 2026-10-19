import { en, fr } from 'vuetify/locale'

export default {
    en: {
        $vuetify: {
            ...en
        },
        title: "Ornipedia",
        subtitle: "The bird encyclopedia",

        filter: "Filters",
        speciesSelect: "Filter by species",
        subSpeciesSelect: "Filter by sub species",
        search: "Search by name",
        close: "Close",
        soon: "Soon",

        a11y: {
            menu: "Open the menu",
            home: "Ornipedia, back to the home page",
            filters: "Filters",
            close: "Close",
            bird_photo: "Bird photo",
        },

        photo: {
            previous: "Previous photo",
            next: "Next photo",
            credit: "Photo:",
            all_of_bird: "All the photos of this bird",
            full_size: "Full size",
        },

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
                desc: "Test your knowledge!"
            }   
        },

        home: {
            banner_alt: "A golden eagle flying in front of snowy mountains",
            search: "Search a bird by name",
            explore: "Explore the gallery",
            stats: "{photos} photos of {species} species",
            highlights: "A few birds",
            see_gallery: "See the whole gallery",
            by_species: "Explore by species",
            coming: "Coming soon",
        },
        footer: {
            credits: "Photos under free licenses, the author and license are shown with each photo.",
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
            title: "Image gallery",
            filters: "Filters",
            no_species: "No match",
            species_chip: "Species: {name}",
            sub_species_chip: "Sub-species: {name}",
            remove_filter: "Remove this filter",
            show_results: "No photo | Show {n} photo | Show {n} photos",
            count: "No photo | {n} photo | {n} photos",
            clear_filters: "Clear the filters",
            error: {
                title: "Unable to load the photos.",
                desc: "Check your connection and try again.",
                retry: "Try again",
            },
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

        filter: "Filtres",
        speciesSelect: "Filtrer par espèce",
        subSpeciesSelect: "Filtrer par sous-espèce",
        search: "Recherche par nom",
        close: "Fermer",
        soon: "Bientôt",

        a11y: {
            menu: "Ouvrir le menu",
            home: "Ornipedia, retour à l'accueil",
            filters: "Filtres",
            close: "Fermer",
            bird_photo: "Photo d'oiseau",
        },

        photo: {
            previous: "Photo précédente",
            next: "Photo suivante",
            credit: "Photo :",
            all_of_bird: "Toutes les photos de cet oiseau",
            full_size: "Pleine résolution",
        },

        settings: "Paramètres",
        settingsTheme: "Thème",
        settingsThemeLight: "Clair",
        settingsThemeDark: "Sombre",
        settingsLanguage: "Langue",

        navigation: {
            home: {
                title: "Accueil",
                desc: "",
            },
            image_gallery: {
                title: "Galerie d'images",
                desc: "Parcourez la galerie d'images"
            } ,
            bird_finder: {
                title:"Trouver un oiseau",
                desc:"Cherchez et trouvez un oiseau"
            } ,
            quiz: {
                title: "Quiz",
                desc: "Testez vos connaissances !"
            }
        },

        home: {
            banner_alt: "Un aigle royal en vol devant des montagnes enneigées",
            search: "Rechercher un oiseau par son nom",
            explore: "Explorer la galerie",
            stats: "{photos} photos de {species} espèces",
            highlights: "Quelques oiseaux",
            see_gallery: "Voir toute la galerie",
            by_species: "Explorer par espèce",
            coming: "Bientôt disponible",
        },
        footer: {
            credits: "Photos sous licences libres, l'auteur et la licence sont indiqués sur chaque photo.",
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
            title: "Galerie d'images",
            filters: "Filtres",
            no_species: "Aucun résultat",
            species_chip: "Espèce : {name}",
            sub_species_chip: "Sous-espèce : {name}",
            remove_filter: "Retirer ce filtre",
            show_results: "Aucune photo | Voir {n} photo | Voir les {n} photos",
            count: "Aucune photo | {n} photo | {n} photos",
            clear_filters: "Effacer les filtres",
            error: {
                title: "Impossible de charger les photos.",
                desc: "Vérifiez votre connexion et réessayez.",
                retry: "Réessayer",
            },
            no_match: {
                title: "Impossible de trouver une image correspondant à votre recherche",
                desc: "Essayez d'ajuster les critères de recherche ou les filtres."
            }
        }
    },
}
