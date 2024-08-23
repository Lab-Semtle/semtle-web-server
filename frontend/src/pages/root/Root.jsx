import axios from "axios";
import React from "react";
import style from "./Root.module.css";

import focusImage from "../../test.jpg";
import { Link } from "react-router-dom";
import Navbarboot from "../../components/Header/Navbarboot";

export default function Root() {
  return (
    <>
      <Navbarboot></Navbarboot>

      <div className={style.focusImage}>
        <img src={focusImage} alt="no file"></img>
      </div>
      <div className={style.contentWrap}>
        <div className={style.titleWrap}>
          <table>
            <tr>
              <th>content1</th>
              <th>content1</th>
              <th>content1</th>
              <th>content1</th>
              <th>content1</th>
              <th>content1</th>
            </tr>
          </table>
        </div>

        <div className={style.cellsWrap}>
          <div className={style.cells}>
            <img src={focusImage} alt="no image"></img>
            <div className={style.cellintroduce}>Curriculum 커리</div>
          </div>

          <div className={style.cells}>
            <img src={focusImage} alt="no image"></img>
            <div className={style.cellintroduce}>오늘의 강의요약</div>
          </div>
          <br />
          <div className={style.cells}>
            <img src={focusImage} alt="no image"></img>
            <div className={style.cellintroduce}>교재 및 ppt 자료</div>
          </div>

          <div className={style.cells}>
            <img src={focusImage} alt="no image"></img>
            <div className={style.cellintroduce}>유저 등급</div>
          </div>
        </div>
      </div>
    </>
  );
}
