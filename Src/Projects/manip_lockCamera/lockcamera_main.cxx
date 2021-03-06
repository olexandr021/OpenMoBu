
/**	\file	lockcamera_main.cxx

Sergei <Neill3d> Solokhin 2018

GitHub page - https://github.com/Neill3d/OpenMoBu
Licensed under The "New" BSD License - https://github.com/Neill3d/OpenMoBu/blob/master/LICENSE


*/

//--- SDK include
#include <fbsdk/fbsdk.h>

#ifdef KARCH_ENV_WIN
	#include <windows.h>
#endif

//--- Library declaration
FBLibraryDeclare( maniplockcamera )
{
	FBLibraryRegister(Manip_LockCamera);
}
FBLibraryDeclareEnd;

/************************************************
 *	Library functions.
 *************** *********************************/
bool FBLibrary::LibInit()		{ return true; }
bool FBLibrary::LibOpen()		{ return true; }
bool FBLibrary::LibReady()		{ return true; }
bool FBLibrary::LibClose()		{ return true; }
bool FBLibrary::LibRelease()	{ return true; }

/**
*	\mainpage	Manipulator Template
*	\section	intro	Introduction
*	Template showing what needs to be done
*	in order to create a new manipulator in FiLMBOX.
*/
