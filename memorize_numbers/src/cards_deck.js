import comete from "./assets/images/comete.png";
import forum from "./assets/images/Forum.png";
import mad from "./assets/images/mad.png";
import te from "./assets/images/TE.jpeg";
import tsm from "./assets/images/tsm.png";
import telespoir from "./assets/images/telespoir.jpeg";
import rezel from "./assets/images/rezel.jpg";
import kft from "./assets/images/kft.png";
import bds from "./assets/images/bds.png";
import bar from "./assets/images/bar.png"; // Cards importation


const cards = [
  { id: 1, name: "comete", image: comete },
  { id: 2, name: "comete", image: comete },
  { id: 3, name: "forum", image: forum },
  { id: 4, name: "forum", image: forum },
  { id: 5, name: "mad", image: mad },
  { id: 6, name: "mad", image: mad },
  { id: 7, name: "te", image: te },
  { id: 8, name: "te", image: te },
  { id: 9, name: "tsm", image: tsm },
  { id: 10, name: "tsm", image: tsm },
  { id: 11, name: "telespoir", image: telespoir },
  { id: 12, name: "telespoir", image: telespoir },
  { id: 13, name: "rezel", image: rezel },
  { id: 14, name: "rezel", image: rezel },
  { id: 15, name: "kft", image: kft },
  { id: 16, name: "kft", image: kft },
  { id: 17, name: "bar", image: bar },
  { id: 18, name: "bar", image: bar },
  { id: 19, name: "bds", image: bds },
  { id: 20, name: "bds", image: bds }

];

export const cardsData = cards.map((card) => ({
  ...card,
  order: Math.floor(Math.random() * 12),
  isFlipped: false,
}));
