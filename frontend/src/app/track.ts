export class Track {
  title: string;
  description: string;
  image_url: string;
  id: number;

  constructor(id: number, title: string, description: string, image_url: string) {
    this.id = id;
    this.title = title;
    this.description = description;
    this.image_url = image_url;
  }

}
