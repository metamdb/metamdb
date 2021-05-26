describe("Flux Model Upload Test", () => {
  beforeEach(() => {
    cy.visit("/mid-calculation");

    const fileName = "reaction-model.csv";

    cy.fixture(fileName).then(fileContent => {
      cy.get("input[type=file]").upload({
        fileContent,
        fileName,
        mimeType: "application/json"
      });
    });
    cy.get("form")
      .contains("Submit")
      .click();
  });

  it("flux model upload header", () => {
    cy.contains("h1", "Upload - Flux Model");
  });

  it("check default upload label", () => {
    cy.get("label").contains("Upload File...");
  });

  it("file required error", () => {
    cy.get("form")
      .contains("Submit")
      .click();
    cy.get(".invalid-feedback").should("contain", "File required");
  });

  it("wrong extension error", () => {
    const fileName = "reaction-model.html";

    cy.fixture(fileName).then(fileContent => {
      cy.get("input[type=file]").upload({
        fileContent,
        fileName,
        mimeType: "application/json"
      });
    });
    cy.get("form")
      .contains("Submit")
      .click();
    cy.get(".invalid-feedback").should("contain", "File format");
  });

  it("api error", () => {
    const fileName = "reaction-model.csv";

    cy.fixture(fileName).then(fileContent => {
      cy.get("input[type=file]").upload({
        fileContent,
        fileName,
        mimeType: "application/json"
      });
    });
    cy.get("form")
      .contains("Submit")
      .click();
    cy.get(".invalid-feedback").should("contain", "NET/EXCHANGE");
  });

  describe("upload flux model", () => {
    const fileName = "flux-model.csv";

    beforeEach(() => {
      cy.fixture(fileName).then(fileContent => {
        cy.get("input[type=file]").upload({
          fileContent,
          fileName,
          mimeType: "application/json"
        });
      });
    });

    it("changed label", () => {
      cy.get("label").contains(fileName);
    });

    it("successful flux model upload", () => {
      cy.get("form")
        .contains("Submit")
        .click()
        .should(() => {
          expect(localStorage.getItem("state")).to.exist;
          const state = JSON.parse(localStorage.getItem("state"));
          expect(state.isFluxModel).to.be.true;
        });
    });
  });
});
