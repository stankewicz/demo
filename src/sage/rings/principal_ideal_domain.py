"""
Abstract base class for principal ideal domains
"""

#*****************************************************************************
#       Copyright (C) 2005 William Stein <wstein@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    General Public License for more details.
#
#  The full text of the GPL is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.rings.ring import PrincipalIdealDomain

def is_PrincipalIdealDomain(R):
    """
    Check if ``R`` is a :class:`PrincipalIdealDomain`.

    EXAMPLES::

        sage: sage.rings.principal_ideal_domain.is_PrincipalIdealDomain(ZZ)
        True
        sage: R.<x,y> = QQ[]
        sage: sage.rings.principal_ideal_domain.is_PrincipalIdealDomain(R)
        False
    """
    return isinstance(R, PrincipalIdealDomain)
