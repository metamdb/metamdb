describe("Reaction Model Upload Test", () => {
  beforeEach(() => {
    cy.visit("/mid-calculation");
  });

  it("reaction model upload header", () => {
    cy.contains("h1", "Upload - Reaction Model");
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

  describe("upload reaction model", () => {
    const fileName = "reaction-model.csv";

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

    it("successful reaction model upload", () => {
      cy.get("form")
        .contains("Submit")
        .click()
        .should(() => {
          expect(localStorage.getItem("state")).to.exist;
          const state = JSON.parse(localStorage.getItem("state"));
          expect(state.isReactionModel).to.be.true;
        });
    });
  });
});
