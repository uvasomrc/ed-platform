import { EdPlatformPage } from './app.po';

describe('ed-platform App', function() {
  let page: EdPlatformPage;

  beforeEach(() => {
    page = new EdPlatformPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
