export class Track {
  title: string;
  description: string;
  image_file: string;
  id: number;

  constructor(id: number, title: string, description: string, image: string) {
    this.id = id;
    this.title = title;
    this.description = description;
    this.image_file = image;
  }

}
