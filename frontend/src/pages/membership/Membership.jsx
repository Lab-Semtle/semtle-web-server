import axios from "axios";
import react, { useEffect, useState } from "react";
import Navbarboot from "../../components/Header/Navbarboot";

export default function Membership() {
  const [email, setEmail] = useState("");
  const [pw, setPw] = useState("");
  const [pw2, setPw2] = useState("");
  const [emailValid, setEmailValid] = useState(false);
  const [pwValid, setPwValid] = useState(false);
  const [pwValid2, setPwValid2] = useState(false);
  const [notAllow, setNotAllow] = useState(true);

  const handleEmail = (e) => {
    setEmail(e.target.value);
    const regex =
      /^(([^<>()\[\].,;:\s@"]+(\.[^<>()\[\].,;:\s@"]+)*)|(".+"))@(([^<>()[\].,;:\s@"]+\.)+[^<>()[\].,;:\s@"]{2,})$/i;

    if (regex.test(email)) {
      setEmailValid(true);
    } else {
      setEmailValid(false);
    }
  };
  const handlePw = (e) => {
    setPw(e.target.value);
    const regex =
      /^(?=.*[a-zA-z])(?=.*[0-9])(?=.*[$`~!@$!%*#^?&\\(\\)\-_=+])(?!.*[^a-zA-z0-9$`~!@$!%*#^?&\\(\\)\-_=+]).{8,20}$/;

    if (regex.test(pw)) {
      setPwValid(true);
    } else {
      setPwValid(false);
    }
  };

  const handlePw2 = (e) => {
    setPw2(e.target.value);
    const regex =
      /^(?=.*[a-zA-z])(?=.*[0-9])(?=.*[$`~!@$!%*#^?&\\(\\)\-_=+])(?!.*[^a-zA-z0-9$`~!@$!%*#^?&\\(\\)\-_=+]).{8,20}$/;

    if (regex.test(pw2)) {
      setPwValid2(true);
    } else {
      setPwValid2(false);
    }
  };

  useEffect(() => {
    if (emailValid && pwValid && pwValid2) {
      setNotAllow(false);
      return;
    }
    setNotAllow(true);
  });

  const onClickConfirmButton = () => {
    if (pw === pw2) {
      axios
        .post("url", {
          email: email,
          pw: pw,
        })
        .then((res) => {
          //console.log(res.data);
        });
    } else return;
  };

  return (
    <div className="page">
      <Navbarboot></Navbarboot>
      <div className="titleWrap">회원가입</div>
      <div className="contentWrap">
        <div className="inputTitle">이메일</div>
        <div className="inputWrap">
          <input
            type="text"
            className="input"
            placeholder="test@gmail.com"
            value={email}
            onChange={handleEmail}
          />
        </div>
        <div className="inputTitle">비밀번호</div>
        <div className="inputWrap">
          <input
            type="password"
            className="input"
            placeholder="********"
            value={pw}
            onChange={handlePw}
          />
        </div>
        <div className="errpr<essageWrap">
          {!emailValid && email.length > 0 && (
            <div>올바른 이메일을 입력해주세요.</div>
          )}
        </div>
        <div className="inputTitle">비밀번호 확인</div>
        <div className="inputWrap">
          <input
            type="password"
            className="input"
            placeholder="********"
            value={pw2}
            onChange={handlePw2}
          />
        </div>

        <div>
          <button
            onClick={onClickConfirmButton}
            className="bottomButton"
            disabled={notAllow}
          >
            확인
          </button>
        </div>
      </div>
    </div>
  );
}
