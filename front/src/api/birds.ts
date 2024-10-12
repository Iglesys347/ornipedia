import instance from "./axios_instance"

export function getBirds() {
    return instance.get("/birds")
}
