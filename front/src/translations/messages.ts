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

        admin: {
            title: "Administration",
            logout: "Log out",
            see: "See",
            login: {
                desc: "Enter the administration password to add birds and photos.",
                password: "Password",
                submit: "Log in",
                errors: {
                    invalid: "Wrong password.",
                    disabled: "The administration is disabled on this server (no password configured).",
                    network: "The server cannot be reached, try again.",
                },
            },
            errors: {
                required: "Required",
                too_big: "The photo must not exceed 25 MB.",
                network: "The server cannot be reached, try again.",
                session: "The password was refused, please log in again.",
                invalid: "Invalid data.",
            },
            photo: {
                tab: "Add a photo",
                tab_short: "Photo",
                bird: "Bird",
                file: "Photo",
                file_hint: "JPEG, PNG or WebP, 25 MB max",
                preview: "Preview of the photo",
                author: "Author",
                author_link: "Link to the author (optional)",
                license: "License (short name)",
                license_full: "Full name of the license",
                license_link: "Link to the license",
                original_url: "Original URL of the photo (optional)",
                submit: "Add the photo",
                added: "Photo added.",
            },
            bird: {
                tab: "Add a bird",
                tab_short: "Bird",
                latin_name: "Latin name",
                name: "Name",
                species: "Species",
                species_hint: "Choose an existing species so that the filters group them",
                sub_species: "Sub-species (optional)",
                details: "Details (optional)",
                submit: "Add the bird",
                added: "Bird added, you can now add its photos.",
            },
            delete: {
                button: "Delete this photo",
                title: "Delete this photo?",
                desc: "The photo is removed from the gallery, this cannot be undone.",
                cancel: "Cancel",
                confirm: "Delete",
                error: "The photo could not be deleted.",
            },
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

        admin: {
            title: "Administration",
            logout: "Se déconnecter",
            see: "Voir",
            login: {
                desc: "Saisissez le mot de passe d'administration pour ajouter des oiseaux et des photos.",
                password: "Mot de passe",
                submit: "Se connecter",
                errors: {
                    invalid: "Mot de passe incorrect.",
                    disabled: "L'administration est désactivée sur ce serveur (aucun mot de passe configuré).",
                    network: "Le serveur est injoignable, réessayez.",
                },
            },
            errors: {
                required: "Obligatoire",
                too_big: "La photo ne doit pas dépasser 25 Mo.",
                network: "Le serveur est injoignable, réessayez.",
                session: "Le mot de passe a été refusé, reconnectez-vous.",
                invalid: "Données invalides.",
            },
            photo: {
                tab: "Ajouter une photo",
                tab_short: "Photo",
                bird: "Oiseau",
                file: "Photo",
                file_hint: "JPEG, PNG ou WebP, 25 Mo maximum",
                preview: "Aperçu de la photo",
                author: "Auteur",
                author_link: "Lien vers l'auteur (optionnel)",
                license: "Licence (nom court)",
                license_full: "Nom complet de la licence",
                license_link: "Lien vers la licence",
                original_url: "URL d'origine de la photo (optionnel)",
                submit: "Ajouter la photo",
                added: "Photo ajoutée.",
            },
            bird: {
                tab: "Ajouter un oiseau",
                tab_short: "Oiseau",
                latin_name: "Nom latin",
                name: "Nom",
                species: "Espèce",
                species_hint: "Choisissez une espèce existante pour que les filtres les regroupent",
                sub_species: "Sous-espèce (optionnel)",
                details: "Détails (optionnel)",
                submit: "Ajouter l'oiseau",
                added: "Oiseau ajouté, vous pouvez maintenant ajouter ses photos.",
            },
            delete: {
                button: "Supprimer cette photo",
                title: "Supprimer cette photo ?",
                desc: "La photo sera retirée de la galerie, c'est définitif.",
                cancel: "Annuler",
                confirm: "Supprimer",
                error: "La photo n'a pas pu être supprimée.",
            },
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
