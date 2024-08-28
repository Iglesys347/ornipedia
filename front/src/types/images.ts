import { BirdInfo } from "./birds";

type LanguageSpecificInfo = {
    [languageCode: string]: BirdInfo;
};

export type ImageInfo = {
    [key: number]: LanguageSpecificInfo;
};
