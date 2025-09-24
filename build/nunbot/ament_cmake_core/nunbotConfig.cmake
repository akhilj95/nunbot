# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_nunbot_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED nunbot_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(nunbot_FOUND FALSE)
  elseif(NOT nunbot_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(nunbot_FOUND FALSE)
  endif()
  return()
endif()
set(_nunbot_CONFIG_INCLUDED TRUE)

# output package information
if(NOT nunbot_FIND_QUIETLY)
  message(STATUS "Found nunbot: 0.0.0 (${nunbot_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'nunbot' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT nunbot_DEPRECATED_QUIET)
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(nunbot_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${nunbot_DIR}/${_extra}")
endforeach()
