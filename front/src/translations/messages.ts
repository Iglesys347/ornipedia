import { en, fr } from 'vuetify/locale'

export default {
    en: {
        $vuetify: {
            ...en
        },
        title: "Ornipedia",
        subtitle: "The bird encyclopedia",

        filter: "Filters",
        groupSelect: "Filter by group",
        subgroupSelect: "Filter by subgroup",
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
            stats: "{photos} photos of {birds} species",
            highlights: "A few birds",
            see_gallery: "See the whole gallery",
            by_group: "Explore by group",
            coming: "Coming soon",
            quiz: {
                title: "Test your knowledge",
                desc: "Recognize birds from their photos, or find a bird's photo from its name. Two difficulty levels: the hard one only mixes birds of the same group.",
                play: "Play the quiz",
            },
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
                commons: "Wikimedia Commons cannot be reached, try again later.",
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
                choose_bird: "Choose the bird first.",
                only_without_photos: "Only the birds without photos ({n})",
                photo_count: "No photo | 1 photo | {n} photos",
                upload_title: "Upload a photo from the computer",
            },
            bird: {
                tab: "Add a bird",
                tab_short: "Bird",
                latin_name: "Latin name",
                optional: "optional, the bird is then only shown in French",
                name: "Name",
                group: "Group",
                group_hint: "Choose an existing group so that the filters gather the birds",
                subgroup: "Subgroup (optional)",
                details: "Details (optional)",
                submit: "Add the bird",
                added: "Bird added, you can now add its photos.",
            },
            commons: {
                title: "From Wikimedia Commons",
                subtitle: "The author and license of the photos are fetched automatically",
                search: "Search on Wikimedia Commons",
                search_hint: "The latin name gives the best results",
                no_result: "No photo found, try another name.",
                already_added: "Already added",
                open: "See on Wikimedia Commons",
                more: "More photos",
                selected: "No photo selected | 1 photo selected | {n} photos selected",
                import: "Add the photos | Add the photo | Add the {n} photos",
                imported: "No photo added | Photo added. | {n} photos added.",
                import_failed: "{added} photo(s) added, {failed} failed.",
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
            title: "Bird quiz",
            intro: "Recognize the birds from their photos, or find the photo of a bird from its name.",
            setup: {
                format: "Quiz format",
                difficulty: "Difficulty",
                length: "Number of questions",
                start: "Start",
            },
            format: {
                photo: { title: "Which bird is it?", desc: "A photo, find the name of the bird among 4 choices." },
                name: { title: "Find the photo", desc: "A bird name, find its photo among 4." },
                mixed: { title: "Mixed", desc: "Both kinds of questions, at random." },
            },
            difficulty: {
                easy: { title: "Easy", desc: "The choices are birds picked at random." },
                hard: { title: "Hard", desc: "The choices are birds of the same group, or even of the same subgroup: telling a golden eagle from a Bonelli's eagle is harder!" },
            },
            progress: "Question {n} / {total}",
            score: "Score: {score}",
            quit: "Quit",
            retry: "Retry",
            question: {
                photo: "Which bird is it?",
                photo_alt: "Photo of the bird to recognize",
                name: "Find the photo of:",
                photo_choice: "Photo {n}",
            },
            feedback: {
                correct: "Well done!",
                wrong: "Missed!",
                it_was: "It was:",
            },
            keyboard_hint: "Tip: use the keys 1 to 4 to answer, and Enter to go on.",
            next: "Next question",
            see_result: "See the result",
            result: {
                perfect: "Perfect score, you are an expert ornithologist!",
                good: "Very good, you know your birds!",
                average: "Not bad, keep practicing!",
                bad: "The birds still have secrets for you, try again!",
            },
            play_again: "Play again",
            change_settings: "Change the settings",
            review: "Your answers",
            your_answer: "Your answer: {name}",
            unknown_author: "unknown author",
            error: {
                not_enough: "There are not enough birds with photos yet to make a quiz.",
                load: "Unable to load the question, please try again.",
            },
        },
        image_gallery: {
            title: "Image gallery",
            filters: "Filters",
            no_result: "No match",
            group_chip: "Group: {name}",
            subgroup_chip: "Subgroup: {name}",
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
        groupSelect: "Filtrer par groupe",
        subgroupSelect: "Filtrer par sous-groupe",
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
            stats: "{photos} photos de {birds} espèces",
            highlights: "Quelques oiseaux",
            see_gallery: "Voir toute la galerie",
            by_group: "Explorer par groupe",
            coming: "Bientôt disponible",
            quiz: {
                title: "Testez vos connaissances",
                desc: "Reconnaissez les oiseaux sur photo, ou retrouvez la photo d'un oiseau à partir de son nom. Deux niveaux : en difficile, seuls des oiseaux du même groupe sont proposés.",
                play: "Jouer au quiz",
            },
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
                commons: "Wikimedia Commons est injoignable, réessayez plus tard.",
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
                choose_bird: "Choisissez d'abord l'oiseau.",
                only_without_photos: "Seulement les oiseaux sans photo ({n})",
                photo_count: "Aucune photo | 1 photo | {n} photos",
                upload_title: "Envoyer une photo depuis l'ordinateur",
            },
            bird: {
                tab: "Ajouter un oiseau",
                tab_short: "Oiseau",
                latin_name: "Nom latin",
                optional: "facultatif, l'oiseau ne sera alors visible qu'en français",
                name: "Nom",
                group: "Groupe",
                group_hint: "Choisissez un groupe existant pour que les filtres regroupent les oiseaux",
                subgroup: "Sous-groupe (optionnel)",
                details: "Détails (optionnel)",
                submit: "Ajouter l'oiseau",
                added: "Oiseau ajouté, vous pouvez maintenant ajouter ses photos.",
            },
            commons: {
                title: "Depuis Wikimedia Commons",
                subtitle: "L'auteur et la licence des photos sont récupérés automatiquement",
                search: "Rechercher sur Wikimedia Commons",
                search_hint: "Le nom latin donne les meilleurs résultats",
                no_result: "Aucune photo trouvée, essayez un autre nom.",
                already_added: "Déjà ajoutée",
                open: "Voir sur Wikimedia Commons",
                more: "Plus de photos",
                selected: "Aucune photo sélectionnée | 1 photo sélectionnée | {n} photos sélectionnées",
                import: "Ajouter les photos | Ajouter la photo | Ajouter les {n} photos",
                imported: "Aucune photo ajoutée | Photo ajoutée. | {n} photos ajoutées.",
                import_failed: "{added} photo(s) ajoutée(s), {failed} en échec.",
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
            title: "Quiz ornitho",
            intro: "Reconnaissez les oiseaux à partir de leurs photos, ou retrouvez la photo d'un oiseau à partir de son nom.",
            setup: {
                format: "Type de quiz",
                difficulty: "Difficulté",
                length: "Nombre de questions",
                start: "Commencer",
            },
            format: {
                photo: { title: "Quel est cet oiseau ?", desc: "Une photo, trouvez le nom de l'oiseau parmi 4 propositions." },
                name: { title: "Trouvez la photo", desc: "Un nom d'oiseau, trouvez sa photo parmi 4." },
                mixed: { title: "Mixte", desc: "Les deux types de questions, au hasard." },
            },
            difficulty: {
                easy: { title: "Facile", desc: "Les propositions sont des oiseaux tirés au hasard." },
                hard: { title: "Difficile", desc: "Les propositions sont des oiseaux du même groupe, voire du même sous-groupe : distinguer un aigle royal d'un aigle de Bonelli, c'est plus dur !" },
            },
            progress: "Question {n} / {total}",
            score: "Score : {score}",
            quit: "Quitter",
            retry: "Réessayer",
            question: {
                photo: "Quel est cet oiseau ?",
                photo_alt: "Photo de l'oiseau à reconnaître",
                name: "Trouvez la photo de :",
                photo_choice: "Photo {n}",
            },
            feedback: {
                correct: "Bravo !",
                wrong: "Raté !",
                it_was: "C'était :",
            },
            keyboard_hint: "Astuce : utilisez les touches 1 à 4 pour répondre, et Entrée pour continuer.",
            next: "Question suivante",
            see_result: "Voir le résultat",
            result: {
                perfect: "Sans faute, vous êtes un ornithologue confirmé !",
                good: "Très bien, vous connaissez vos oiseaux !",
                average: "Pas mal, continuez à vous entraîner !",
                bad: "Les oiseaux ont encore des secrets pour vous, réessayez !",
            },
            play_again: "Rejouer",
            change_settings: "Changer les paramètres",
            review: "Vos réponses",
            your_answer: "Votre réponse : {name}",
            unknown_author: "auteur inconnu",
            error: {
                not_enough: "Il n'y a pas encore assez d'oiseaux avec photos pour faire un quiz.",
                load: "Impossible de charger la question, réessayez.",
            },
        },
        image_gallery: {
            title: "Galerie d'images",
            filters: "Filtres",
            no_result: "Aucun résultat",
            group_chip: "Groupe : {name}",
            subgroup_chip: "Sous-groupe : {name}",
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
