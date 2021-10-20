import update from "immutability-helper";

export const mainReducer = (state, action) => {
  switch (action.type) {
    case "UPLOAD_REACTION_MODEL":
      return {
        ...state,
        isReactionModel: true,
        reactions: action.payload.data.reactions,
      };
    case "DELETE_REACTION_MODEL":
      return {
        ...state,
        isReactionModel: false,
        reactions: null,
      };
    case "UPDATE_ATOM_MAPPING":
      return update(state, {
        reactions: {
          [action.payload.rowIndex]: {
            mappings: {
              [action.payload.currentMapping]: {
                [action.payload.index]: {
                  [action.payload.key]: { $set: action.payload.value },
                },
              },
            },
          },
        },
      });
    default:
      return state;
  }
};

export const authReducer = (state, action) => {
  switch (action.type) {
    case "LOGIN":
      localStorage.setItem("token", action.payload.token);
      return {
        id: action.payload.id,
        name: action.payload.name,
        orcid: action.payload.orcid,
        role: action.payload.role,
        isUser: true,
      };
    case "LOGOUT":
      localStorage.removeItem("token");
      return {
        id: null,
        name: null,
        orcid: null,
        role: null,
        isUser: false,
      };
    default:
      return state;
  }
};
