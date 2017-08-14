export class Track {
  private title: string;
  private description: string;
  private image_file: string;
  private id: number;

  constructor(id:number, title:string, description:string, image:string) {
    this.id = id;
    this.title = title;
    this.description = description;
    this.image_file = image;
  }

}
