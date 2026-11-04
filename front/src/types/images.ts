type Bird = {
    id: number;
    name: string;
    group: string;
    subgroup: string | null;
    details: string;
    language_code: string;
    latin_name: string;
}

type License = {
    short_name: string;
    full_name: string;
    link: string;
}

type Author = {
    name: string;
    link: string;
}

export type ImageInfo = {
    id: number;
    bird: Bird;
    license: License;
    author : Author;
    original_url: string
};

type LanguageSpecificInfo = {
    [languageCode: string]: ImageInfo;
};

export type ImagesInfo = {
    [key: number]: LanguageSpecificInfo;
};
