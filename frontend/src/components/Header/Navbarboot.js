import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Link } from 'react-router-dom';


function Navbarboot() {
  return (

      <Navbar collapseOnSelect expand="lg" className="bg-body-tertiary">
        <Container>
          <Navbar.Brand as={Link} to="/Main">Semtle</Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link as={Link} to="/Board">게시판</Nav.Link>
              <Nav.Link href="#pricing">교수님</Nav.Link>
              <NavDropdown title="더보기" id="collapsible-nav-dropdown">
                <NavDropdown.Item href="#action/3.1">sememem</NavDropdown.Item>
                <NavDropdown.Item href="#action/3.2">
                  sdfdsfsdf
                </NavDropdown.Item>
                <NavDropdown.Item href="#action/3.3">sdfsdf</NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item href="#action/3.4">
                  sdfddfsd
                </NavDropdown.Item>
              </NavDropdown>
            </Nav>
            <Nav>
              <Nav.Link href="#deets">내 정보</Nav.Link>
              <Nav.Link eventKey={2} href="#memes">
                로그인
              </Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

  );
}

export default Navbarboot;