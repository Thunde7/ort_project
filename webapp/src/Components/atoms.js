import { atom, selector } from "recoil";

export const tokenState = atom({
  key: "currentUser/tokenState",
  default : "",
});