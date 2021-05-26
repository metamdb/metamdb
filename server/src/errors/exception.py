"""Custom exceptions."""

from typing import List, Optional, Union


class AtomMappingError(Exception):
    """Base exception for errors raised by atom mappings"""
    def __init__(self,
                 reaction: Union[str, List[str]],
                 message: Optional[str] = None):
        if message is None:
            if isinstance(reaction, list):
                message = "An atom mapping error occured in reactions: %s" % ', '.join(
                    reaction)
            else:
                message = "An atom mapping error occured in reaction: %s" % reaction

        super(AtomMappingError, self).__init__(message)
        self.reaction = reaction


class MissingAtomMappingError(AtomMappingError):
    """Atom mapping errors caused by missing mapping"""
    def __init__(self, reaction: Union[str, List[str]]):
        if isinstance(reaction, list):
            message = "An atom mapping is missing in reactions: %s" % ', '.join(
                reaction)
        else:
            message = "An atom mapping is missing in reaction: %s" % reaction

        super(MissingAtomMappingError, self).__init__(reaction, message)


class ReactantError(AtomMappingError):
    """Atom mapping errors caused by unequal/no reactants"""
    def __init__(self, reaction: str, reactant: str):
        message = "%s: No atom mapping for the reactant %s" % (reaction,
                                                               reactant)

        super(ReactantError, self).__init__(reaction, message)
        self.reactant = reactant


class CodeOutOfBoundsError(AtomMappingError):
    """Printable characters too short for necessary atom mapping code"""
    def __init__(self, reaction: str):
        message = "%s: Atom mapping too long for printable characters, unable to generate atom mapping" % reaction

        super(CodeOutOfBoundsError, self).__init__(reaction, message)


class DatabaseError(AtomMappingError):
    """Atom mapping in the database is inaccurate"""
    def __init__(self, reaction: str):
        message = "%s: Database atom mapping is inaccurate" % reaction

        super(DatabaseError, self).__init__(reaction, message)


class LabelingSimulationError(Exception):
    """Base exception for errors raised by labeling simulation"""
    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "An error occured during the process of labeling simulation"

        super(LabelingSimulationError, self).__init__(message)


class SingularMatrixError(LabelingSimulationError):
    """Uploaded flux model and reaction model cant be solved"""
    def __init__(self):
        message = f"Uploaded flux model and reaction model cant be solved due to a 'singular matrix error'"

        super(SingularMatrixError, self).__init__(message)


class ReactionModelError(Exception):
    """Base exception for errors raised by reaction model generation"""
    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "An error occured during the process of reaction model generation"

        super(ReactionModelError, self).__init__(message)


class NoFluxTypeError(ReactionModelError):
    """Uploaded model has no flux type"""
    def __init__(self):
        message = "Fluxes can't be identified, you have no flux type. The flux type has to be either 'FORWARD/REVERSE' or 'NET/EXCHANGE'"

        super(NoFluxTypeError, self).__init__(message)


class FluxModelIdentificationError(ReactionModelError):
    """Uploaded flux model cant be identified"""
    def __init__(self, first_header: str, second_header: str):
        header = f"{first_header}/{second_header}"
        message = f"Flux model cant be identified, your header '{header}' is neither 'FORWARD/REVERSE' nor 'NET/EXCHANGE'"

        super(FluxModelIdentificationError, self).__init__(message)
        self.header = header